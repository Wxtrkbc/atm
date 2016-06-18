#!/usr/bin/env python
# coding=utf-8
import socket
import sys
import hashlib

class AtmClient:
    def __init__(self, address):
        self.address = AtmClient.get_ip_port(address)

        self.message = '\t1、消费\n\t2、提现\n\t3、还款\n\t4、转账\n\t5、查看\n\tq、离开'
        self.dict = {
            '1': self.consume,
            '2': self.withdraw,
            '3': self.repay,
            '4': self.transfer,
            '5': self.view,
        }

    @staticmethod
    def get_ip_port(address):
        ip, port = address.split(':')
        return (ip, int(port))

    @staticmethod
    def isfloat(inp):
            try:
                float(inp)
            except Exception as e:
                return False
            else:
                return True

    def login(self):
        try_counts = 0
        while try_counts < 3:
            cardid = input('请输入卡号：')
            self.cardid = cardid  # 保存该用户的卡号信息
            if len(cardid) == 0:
                continue
            passwd = input('请输入用密码：')
            if len(passwd) == 0:
                continue
            pd = hashlib.sha256()
            pd.update(passwd.encode())
            self.socket.sendall('login|{}:{}'.format(cardid, pd.hexdigest()).encode())  # 发送加密后的账户信息
            ret = self.socket.recv(1024).decode()
            if ret == '200':
                print('登陆成功！')
                return True
            elif ret == '203':
                print('账户不存在')
                try_counts += 1
            else:
                print('用户名或密码错误请重新输入：')
                try_counts += 1
        sys.exit("Too many attemps")

    def internet(self):
        while True:
            print(self.message)
            inp = input('[请输入你的选项]:')
            if inp == 'q':
                break
            elif inp in self.dict:
                self.dict[inp]()
            else:
                print('你输入的选项有误，请重新输入')

    def repay(self):
        inp = input('请输入还款金额：')
        if AtmClient.isfloat(inp):
            self.socket.sendall(('repay|{}'.format(inp)).encode())
            data = self.socket.recv(1024).decode()
            print(data)
        else:
            print('你输入的金额有误，请重新操作')

    def withdraw(self):    # 提现
        inp = input('请输入提现金额：')
        if AtmClient.isfloat(inp):
            self.socket.sendall(('withdraw|{}'.format(inp)).encode())
            data = self.socket.recv(1024).decode()
            print(data)
        else:
            print('你输入的金额有误，请重新操作')

    def consume(self):  # 消费
        inp = input('请输入消费金额：')
        if AtmClient.isfloat(inp):
            self.socket.sendall(('consume|{}'.format(inp)).encode())
            data = self.socket.recv(1024).decode()
            print(data)
        else:
            print('你输入的金额有误，请重新操作')

    def transfer(self):          # 转账
        cardid = input("请输入对方的卡号：")
        money = input('请输入转账金额：')
        if AtmClient.isfloat(money):
            self.socket.sendall(('transfer|{}:{}'.format(cardid, money)).encode())
            ret =self.socket.recv(1024).decode()
            if ret == '300':
                print('对方卡号不存在')
            elif ret == '301':
                print('转账成功')
            else:
                print('余额不足')
        else:
            print('你输入的金额有误，请重新操作')

    def view(self):
        self.socket.sendall('view'.encode())
        data = self.socket.recv(1024).decode()
        print(data)

    def start(self):
        self.socket = socket.socket()
        try:
            self.socket.connect(self.address)
        except Exception as e:
            sys.exit("Failed to connect server:%s" % e)

        print('\t1、登陆\n\t2、离开')
        inp = input('请输入你选项:')
        if inp == '1':
            if self.login():  # 登陆成功后进行交互操作
                self.internet()
        else:
            sys.exit()