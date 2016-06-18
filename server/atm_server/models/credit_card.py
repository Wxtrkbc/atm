#!/usr/bin/env python
# coding=utf-8

import time

class CreditCard:
    def __init__(self, user, passwd, card_id, limit, ):
        self.user = user
        self.passwd = passwd
        self.card_id = card_id
        self.credit_limit = limit                       # 信用卡可用额度
        self.saving = 0                                 # 账户余额
        self.balance = limit                            # 信用卡额度
        self.before_debt = 10000                        # 以前的欠款, 为了便于程序测试，设置为10000
        self.now_debt = 0                               # 本月透支的欠款
        self.interest = self.before_debt * 0.0005       # 本月每天的利息
        self.total_interest = 0                         # 总的利息
        self.flag = 0                                   # (0代表正常，1代表账户冻结)

    def show_info(self):
        str = '用户名:{} ' \
              '卡号:{} ' \
              '可用额度:{:<8} ' \
              '账户余额:{:<8}' \
              '总欠款:{:<8} ' \
              '日利息:{:<4} ' \
              '是否冻结:{}'.format(self.user, self.card_id, self.credit_limit, self.saving, self.before_debt,
                                  self.interest, self.flag)
        return str

    def subtransfer(self, num):  # 转账到其他账户
        if self.saving >= num:
            self.saving -= num
            return True
        elif self.credit_limit > (num - self.saving)*(1 + 0.05):
            temp = num - self.saving
            self.saving = 0
            self.credit_limit -= temp*(1+0.05)
            return True
        else:
            return False

    def addtransfer(self, num):  # 其他账户转到本卡
        self.saving += num
        return True

    def withdraw(self, num):  # 提现,提现收取0.05的手续费
        # if self.saving >= (num + num * 0.05):
        #     self.saving -= num
        #     self.saving -= num * 0.05
        #     return True
        if self.saving >= num:
            self.saving -= num
            return True
        else:
            temp = num - self.saving
            if self.credit_limit >= (temp + temp * 0.05):
                self.credit_limit -= temp
                self.credit_limit -= temp * 0.05
                self.saving = 0
                self.now_debt = temp + temp * 0.05
                return True
            else:
                return False

    def consume(self, num):  # 消费
        if self.saving >= num:
            self.saving -= num
            return True
        else:
            temp = num - self.saving
            if self.credit_limit >= temp:
                self.credit_limit -= temp
                self.saving = 0
                self.now_debt = temp
                return True
            else:
                return False

    def repay(self, num):  # 还款，
        if num > self.before_debt:
            self.interest = 0
            temp1 = num - self.before_debt
            self.before_debt = 0
            if temp1 > self.now_debt:
                self.now_debt = 0
                self.credit_limit = 15000
                self.saving += temp1
                self.before_debt = 0
            else:
                self.before_debt = 0
                self.now_debt -= temp1
                self.credit_limit = 15000 - self.now_debt
        else:
            self.before_debt -= num
        return True

    def everyday_auto(self):
        if self.before_debt > 0:
            self.total_interest += self.interest
        struct_time = time.localtime()
        if struct_time.tm_mday == 11:
            temp = self.now_debt + self.total_interest
            self.before_debt += temp
            self.now_debt = 0
            self.total_interest = 0
            self.credit_limit = 15000  # 恢复额度
