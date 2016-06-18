#!/usr/bin/env python
# coding=utf-8

import socket
import sys
import hashlib
import json
import hashlib


class SupermarketClient:
    def __init__(self, address):
        self.address = SupermarketClient.get_ip_port(address)
        self.cars = {}
        self.message = ' 1、查看商品列表\n 2、选择商品到购物车\n 3、从购物车移除商品\n 4、查看购物车\n 5、结算'
        self.funcdict = {
            '1': self.viewitem,
            '2': self.apenditem,
            '3': self.removeitem,
            '4': self.viewcars,
            '5': self.payitem,
        }

    @staticmethod
    def get_ip_port(address):
        ip, port = address.split(':')
        return (ip, int(port))

    def register(self):
        try_counts = 0
        while try_counts < 3:
            user = input('请输入用户名：')
            # user = 'kobe'
            if len(user) == 0:
                continue
            passwd = input('请输入用密码：')
            # passwd = '123'
            if len(passwd) == 0:
                continue
            pd = hashlib.sha256()
            pd.update(passwd.encode())
            self.socket.sendall('register|{}:{}'.format(user, pd.hexdigest()).encode())  # 发送加密后的账户信息
            ret = self.socket.recv(1024).decode()
            if ret == '202':
                print('注册成功请登录')
                return True
            else:
                try_counts += 1
        sys.exit("Too many attemps")

    def login(self):
        try_counts = 0
        while try_counts < 3:
            user = input('请输入用户名：')
            # user = 'kobe'
            self.user = user
            if len(user) == 0:
                continue
            passwd = input('请输入用密码：')
            # passwd = '123'
            if len(passwd) == 0:
                continue
            pd = hashlib.sha256()
            pd.update(passwd.encode())
            self.socket.sendall('login|{}:{}'.format(user, pd.hexdigest()).encode())  # 发送加密后的账户信息
            ret = self.socket.recv(1024).decode()
            if ret == '200':
                print('登陆成功！')
                self.cwd = self.socket.recv(1024).decode()
                return True
            else:
                try_counts += 1
        sys.exit("Too many attemps")

    def internet(self):
        while True:
            print(self.message)
            inp = input('[请输入你的选项q(uit)]:')
            if inp in self.funcdict:
                self.funcdict[inp]()
            elif inp == 'q':
                break
            else:
                print('你输入的选项有误，请重新输入')

    def viewcars(self):
        for k, v in self.cars.items():
            print(k, v)

    def apenditem(self):  # 添加商品
        for num, item in enumerate(self.goods_list, 1):
            print('\t\t{} {} 价格:{}'.format(num, item['name'], item['price']))
        inp = input('请输入你要购买的商品选项：')
        if int(inp) < len(self.goods_list):
            name = self.goods_list[int(inp)-1]['name']
            num = input('请输入你要购买的商品数量：')
            self.cars[name] = int(num)
            self.socket.sendall(('apenditem|{}:{}'.format(name, num)).encode())
        else:
            print('你输入的选项有误，请重新操作')

    def removeitem(self):  # 移除商品
        for k, v in self.cars.items():
            print(k, v)
        name = input('请输入你想移除的商品名称：')
        num = input('请输入你想移除的商品数量：')
        if self.cars[name] >= int(num):
            self.cars[name] -= int(num)
            self.socket.sendall(('removeitem|{}:{}'.format(name, num)).encode())
        else:
            print('你输入的商品数量有误，请重新操作！')
        print(self.cars)

    def viewitem(self):  # 显示商品
        self.socket.sendall('viewitem|'.encode())
        data = json.loads(str(self.socket.recv(1024), encoding='utf-8'))
        self.goods_list = data
        for num, item in enumerate(data, 1):
            print('\t\t{} {} 价格:{}'.format(num, item['name'], item['price']))


    def payitem(self):  # 结算
        cardid = input('请输入你的卡号：')
        passwd = input('请输入你的密码：')
        self.socket.sendall(('payitem|{}:{}'.format(cardid, passwd)).encode())
        if self.socket.recv(1024).decode() == '刷卡成功':
            print('购买成功')
        else:
            print('余额不足，购买失败，请重新操作')

    def start(self):
        self.socket = socket.socket()
        try:
            self.socket.connect(self.address)
        except Exception as e:
            sys.exit("Failed to connect server:%s" % e)
        print(self.socket.recv(1024).decode())
        print('\t1、注册\n\t2、登录\n\t3、离开： ')
        inp = input('请输入你的选项：')
        # inp = '2'
        if inp == '1':
            if self.register():
                if self.login():  # 登陆成功后进行交互操作
                    self.internet()
        elif inp == '2':
            if self.login():
                self.internet()
        else:
            sys.exit()
