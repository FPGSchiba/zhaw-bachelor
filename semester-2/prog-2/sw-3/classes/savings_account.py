# -*- coding: utf-8 -*-
"""
PROG2 P02 1.1: Comments and prints

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

from bank_account import BankAccount

class SavingsAccount(BankAccount):
    def __init__(self):
        self.limit_overcharge_interest = 0.0
        super().__init__()
        print('Savings Account')

if __name__ == '__main__':
    savingsAccount = SavingsAccount()
    print(savingsAccount.balance)


