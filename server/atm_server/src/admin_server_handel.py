#!/usr/bin/env python
# coding=utf-8

import os
import sys
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pickle
import random
from models import credit_card
from conf import settings
import hashlib


class Handel:
    def __init__(self):
        self.dict1 = {
            '1': self.register,
            '2': self.view,
            '3': self.opera,
            '4': self.myexit
        }

    @staticmethod
    def make_card_num():  # 随机生成一个卡号
        tmp = ''
        for i in range(11):
            n = random.randrange(1, 10)
            tmp += str(n)
        return int(tmp)

    def register(self):  # 注册用户
        username = input('请输入注册者用户名：')
        passwd = input('请输入注册者密码：')
        cardid = Handel.make_card_num()
        limit = input('请输入透支额度：')

        pd = hashlib.sha256()
        pd.update(passwd.encode())

        cretobj = credit_card.CreditCard(username, pd.hexdigest(), cardid, int(limit))  # 创建以该用户封装的行用卡的对象
        cardpath = os.path.join(settings.USER_USER_INFO_DIR, str(cardid))
        os.mkdir(cardpath)
        cardpathcored = os.path.join(cardpath, 'record')
        os.mkdir(cardpathcored)
        cardpathinfo = os.path.join(cardpath, str(cardid))
        try:
            f = open(cardpathinfo, 'xb')  # 以x模式打开,不存在的话，说明这张卡还没有被注册
            pickle.dump(cretobj, f)
            print('用户注册成功卡号为{}'.format(cardid))
        except Exception as e:
            f.close()
        finally:
            f.close()

    def view(self):  # 查看账户
        inp = input('请输入你要查看的账户卡号：')
        cardidpath = os.path.join(settings.USER_USER_INFO_DIR, inp, inp)
        if os.path.exists(cardidpath):
            f = open(cardidpath, 'rb')
            cardobj = pickle.load(f)
            if cardobj.flag == 1:
                print('该用户已冻结')
            print(cardobj.show_info())
            f.close()
        else:
            print('你输入的卡号有误，请重新操作')


    def opera(self):  # 冻结或销户
        inp = input('请输入你要操作的账户卡号：')
        cardidpath = os.path.join(settings.USER_USER_INFO_DIR, inp, inp)
        if os.path.exists(cardidpath):
            # f = open(cardidpath, 'w+b')
            cardobj = pickle.load(open(cardidpath, 'rb'))
            print(cardobj.flag)
            print('\t1、冻结\n\t2、解冻\n\t3、销户\n\t4、离开')
            choice = input('请输入你的选项：')
            if choice == '1':
                cardobj.flag = 1
                pickle.dump(cardobj, open(cardidpath, 'wb'))
                print(cardobj.flag)
                print('已冻结该账户')
            elif choice == '2':
                cardobj.flag = 0
                pickle.dump(cardobj, open(cardidpath, 'wb'))
                print('该账户已解冻')
            elif choice == '3':
                os.remove(cardidpath)
                print('该账户已销户')
            else:
                pass
        else:
            print('你输入的卡号有误，请重新操作')

    def myexit(self):
        sys.exit()
