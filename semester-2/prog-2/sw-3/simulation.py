# -*- coding: utf-8 -*-
"""
PROG2 P02 1.1: Comments and prints

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""
import datetime
import time

from classes.youth_account import YouthAccount
from classes.savings_account import SavingsAccount

if __name__ == '__main__':
    ya1 = YouthAccount(datetime.date(2020, 1, 1))
    try:
        ya2 = YouthAccount(datetime.date(1980, 1, 1))
    except ValueError as err:
        print(err)
    ya1.deposit(10000)
    time.sleep(10)
    ya1.withdraw(2200)
    sa = SavingsAccount()
    sa.deposit(100)
    time.sleep(10)
    ya1.withdraw(-100)
    time.sleep(10)
    print(f'Savings Account Balance: {sa.retrieve_balance()}')
    print(f'Youth Account Balance: {ya1.retrieve_balance()}')
    sa.withdraw(200)
    sa.deposit(50)
    time.sleep(10)
    print(f'Savings Account Balance: {sa.retrieve_balance()}')
    print(f'Youth Account Balance: {ya1.retrieve_balance()}')
    print(sa)
    print(ya1)
