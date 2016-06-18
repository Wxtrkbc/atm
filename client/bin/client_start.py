#!/usr/bin/env python
# coding=utf-8

# !/usr/bin/env python
# coding=utf-8
import socket
import hashlib

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src import atm_client, supermart_client


def main():
    # address = input('请输入FTP服务端地址(ip:port)：')
    print('有以下选选项：\n\t1、登陆银行服务端\n\t2、登陆购物商城\n\t3、离开')
    inp = input('请输入你的选项：')
    if inp == '1':
        address = '127.0.0.1:9999'
        client = atm_client.AtmClient(address)
        client.start()
    elif inp == '2':
        address = '127.0.0.1:8888'
        client = supermart_client.SupermarketClient(address)
        client.start()
    else:
        sys.exit()

if __name__ == '__main__':
    main()
