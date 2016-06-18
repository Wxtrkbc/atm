#!/usr/bin/env python
# coding=utf-8

import socketserver
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from conf import settings
import json
import socket
import hashlib

class Myhandel(socketserver.BaseRequestHandler):
    def handle(self):
        self.goods = [
            {"name": "电脑", "price": 1999},
            {"name": "鼠标", "price": 10},
            {"name": "游艇", "price": 20},
            {"name": "美女", "price": 998},
        ]
        self.good_price = {i['name']: i['price'] for i in self.goods}  # 生成物品价格字典
        self.cars = {"电脑": 0, "鼠标": 0, "游艇": 0, "美女": 0}
        self.request.sendall('欢迎来到购物商城！'.encode())
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

    def viewitem(self, argv=None):  # 返回给客户端商品列表
        self.request.sendall(bytes(json.dumps(self.goods), encoding='utf-8'))

    def apenditem(self, argv=None):  # 添加商品
        name, num = argv.split(':')
        self.cars[name] += int(num)
        print(self.cars)

    def removeitem(self, argv=None):  # 删除商品
        name, num = argv.split(':')
        self.cars[name] -= int(num)
        print(self.cars)

    def payitem(self, argv=None):  # 结算
        cardid, passwd = argv.split(':')
        pd = hashlib.sha256()
        pd.update(passwd.encode())
        sum = 0
        for i in self.cars:
            sum += self.good_price[i]*self.cars[i]    # 计算购物车商品价格
        print(sum)
        s = socket.socket()
        address = ('127.0.0.1', 9999)
        s.connect(address)

        s.sendall('login|{}:{}'.format(cardid, pd.hexdigest()).encode())
        ret = s.recv(1024).decode()
        print(ret)
        if ret == '200':
            s.sendall(bytes('consume|{}'.format(sum), encoding='utf-8'))
            ret1 = s.recv(1024).decode()
            if ret1 == '刷卡成功':
                self.request.sendall(bytes('刷卡成功', encoding='utf-8'))
        else:
            self.request.sendall(bytes('刷卡失败', encoding='utf-8'))
        s.close()

    def register(self, argv=None):
        response_code = '202'
        username, _ = argv.split(':')  # 取出用户名
        f = open(settings.USER_DB_DIR, 'a+')  # 以a+模式打开的时候，指针已经到最后l
        f.seek(0)
        for line in f:
            if username == line.strip().split(':')[0]:
                response_code = '203'  # 注册失败
        if response_code == '202':
            f.write('\n' + argv)
        self.request.sendall(response_code.encode())

    def login(self, argv):
        print(argv, 999)
        username, _ = argv.split(':')
        self.username = username
        with open(settings.USER_DB_DIR, 'r') as f:
            response_code = '201'
            for line in f:
                if argv == line.strip():
                    response_code = '200'  # 认证成功
        self.request.sendall(response_code.encode())
        if response_code == '200':
            self.request.sendall(bytes(os.getcwd(), encoding='utf-8'))


if __name__ == '__main__':
    address = ('127.0.0.1', 8888)
    server = socketserver.ThreadingTCPServer(address, Myhandel)
    server.serve_forever()
