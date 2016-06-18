#!/usr/bin/env python
# coding=utf-8

import os
import sys
import pickle

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from conf import settings
from models import credit_card

user_path = settings.USER_USER_INFO_DIR

l = os.listdir(user_path)

for i in l:
    cardobj_path = os.path.join(user_path, i, i)
    print(cardobj_path)
    if os.path.isfile(cardobj_path):
        # f = open(cardobj_path, 'w+b')
        cardobj = pickle.load(open(cardobj_path, 'rb'))
        cardobj.everyday_auto()
        pickle.dump(cardobj, open(cardobj_path, 'wb'))



# f = open(os.path.join(user_path, '61218852813', '61218852813'), 'rb')
# obj = pickle.load(f)
# print(obj.total_interest)

