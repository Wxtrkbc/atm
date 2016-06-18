#!/usr/bin/env python
# coding=utf-8

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from conf import settings
import hashlib
from src import admin_server_handel

def login():
    trycounts = 0
    while trycounts < 3:
        adminuser = input('请输入管理员账户：')
        adminpd = input('请输入管理员账户密码：')
        pd = hashlib.sha256()
        pd.update(adminpd.encode())
        str = adminuser + ':' + pd.hexdigest()
        with open(settings.ADMIN_INFO_DIR, 'r') as f:
            for line in f:
                if str == line.strip():
                    print('登陆成功')
                    return True
        print('密码或账户错误，请重新输入：')
        trycounts += 1
    print('too many times')
    return False


def main():
    print('欢迎登陆银行管理系统！')
    if login():
        admin_handel = admin_server_handel.Handel()
        while True:
            print('\t1、录入账户\n\t2、查看账户\n\t3、冻结或销户\n\t4、离开')
            inp = input('[请输入你的选项:]')
            if inp in admin_handel.dict1:
                admin_handel.dict1[inp]()
            else:
                print('你的输入的选项有误，请重新输入！')
    else:
        pass


if __name__ == '__main__':
    main()

