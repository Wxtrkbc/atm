#!/usr/bin/env python
# coding=utf-8

import os
import sys
import logging
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from conf import settings


def recode_msg(card_num, message):
    struct_time = time.localtime()
    if struct_time.tm_mday < 23:
        file_name = "%s_%s_%d" % (struct_time.tm_year, struct_time.tm_mon, 22)
    else:
        file_name = "%s_%s_%d" % (struct_time.tm_year, struct_time.tm_mon + 1, 22)

    file_handler = logging.FileHandler(
        os.path.join(settings.USER_USER_INFO_DIR, card_num, 'record', file_name),
        encoding='utf-8'
    )
    fmt = logging.Formatter(fmt="%(asctime)s :  %(message)s")
    file_handler.setFormatter(fmt)

    logger = logging.Logger('user_logger', level=logging.INFO)
    logger.addHandler(file_handler)
    logger.info(message)
