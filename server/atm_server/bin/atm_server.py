#!/usr/bin/env python
# coding=utf-8

import socketserver
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src import atm_server_handel

if __name__ == '__main__':
    address = ('127.0.0.1', 9999)
    server = socketserver.ThreadingTCPServer(address, atm_server_handel.Myhandle)
    server.serve_forever()
