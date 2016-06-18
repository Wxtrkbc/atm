#!/usr/bin/env python
# coding=utf-8

import socketserver
import os
import sys

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pickle
from models import credit_card, log
from conf import settings


class Myhandle(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024).decode()
            if '|' in data:
                cmd, argv = data.split('|')
            else:
                cmd = data
                argv = None
            self.process(cmd, argv)  # 所有的处理先经过 process

    def process(self, cmd, argv=None):  # 使用反射处理客户端传过来的命令（自定义的命令）
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            func(argv)

    @staticmethod
    def open(cardid):
        cardpath = os.path.join(settings.USER_USER_INFO_DIR, cardid, cardid)
        if os.path.exists(cardpath):
            f = open(cardpath, 'rb')
            cardobj = pickle.load(f)
            return cardobj
        else:
            return False

    @staticmethod
    def save(cardobj):
        cardpath = os.path.join(settings.USER_USER_INFO_DIR, str(cardobj.card_id), str(cardobj.card_id))
        f = open(cardpath, 'wb')
        pickle.dump(cardobj, f)

    def repay(self, argv=None):  # 还款
        if self.cardobj.repay(int(argv)):
            log.recode_msg(str(self.cardobj.card_id), '{}还款{}'.format(self.cardobj.show_info(), argv))
            self.request.sendall('还款成功'.encode())
            Myhandle.save(self.cardobj)
        else:
            self.request.sendall('余额不足'.encode())

    def withdraw(self, argv=None):
        if self.cardobj.withdraw(int(argv)):
            log.recode_msg(str(self.cardobj.card_id), '{}提取现金{}'.format(self.cardobj.show_info(), argv))
            self.request.sendall('提取现金成功'.encode())
            Myhandle.save(self.cardobj)
        else:
            self.request.sendall('余额不足'.encode())

    def consume(self, argv=None):
        if self.cardobj.consume(int(argv)):
            log.recode_msg(str(self.cardobj.card_id), '{}消费{}'.format(self.cardobj.show_info(), argv))
            self.request.sendall('刷卡成功'.encode())
            Myhandle.save(self.cardobj)
        else:
            self.request.sendall('余额不足'.encode())

    def transfer(self, argv=None):
        othercardid, money = argv.split(':')
        othercardobj = Myhandle.open(othercardid)
        if othercardobj == False:
            response_code = '300'                  # 对方卡号不存在
        else:
            if self.cardobj.subtransfer(int(money)):       # 自己的卡如果钱够的话，减少自己卡的钱
                if othercardobj.addtransfer(int(money)):
                    log.recode_msg(str(self.cardobj.card_id), '转入其他账户{}：{}'.format(othercardid, money))
                    response_code = '301'  # 转账成功
                    self.save(self.cardobj)
                    self.save(othercardobj)
            else:
                response_code = '302'             # 转账失败余额不足
        self.request.sendall(response_code.encode())

    def view(self, argv=None):
        self.request.sendall('{}'.format(self.cardobj.show_info()).encode())

    def login(self, argv):
        cardid, passwd = argv.split(':')
        cardobj = Myhandle.open(cardid)
        if cardobj == False:
            response_code = '203'   # 账户不存在
        else:
            self.cardid = str(cardobj.card_id)
            if cardobj.passwd == passwd and cardobj.card_id == int(cardid):
                response_code = '200'           # 登陆成功
                self.cardobj = cardobj
            else:
                response_code = '201'           # 用户密码错误
        self.request.sendall(response_code.encode())
