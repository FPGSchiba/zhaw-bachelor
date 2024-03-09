# -*- coding: utf-8 -*-
"""
PROG2 P02 1.1: Comments and prints

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

import math
import random
import string
import datetime


class BankAccount:
    def __init__(self):
        self.IBAN = 'CH' + ''.join(random.choice(string.digits) for _ in range(19))
        self.balance = 0.0
        self.open = True
        self.currency = ("Fr.", "Rp.")
        self.interest = 0.001  # More Savings then youth accounts -> defaults to savings
        self.current_month, _ = divmod(datetime.datetime.now().second, 10)


    def open_account(self) -> bool:
        if not self.open:
            self.open = True
            return True
        elif self.open:
            return False

    def close_account(self) -> bool:
        if self.open:
            self.open = False
            return True
        elif not self.open:
            return False

    def deposit(self, amount: float) -> str:
        if self.balance + amount > 100000:
            return self.retrieve_balance()
        self.balance = self.balance + amount
        return self.retrieve_balance()

    def withdraw(self, amount: float) -> str:
        if self.balance - amount <= 0:
            return self.retrieve_balance()
        self.balance = self.balance - amount
        return self.retrieve_balance()

    def retrieve_balance(self) -> str:
        main_currency = math.floor(self.balance)
        second_currency = (self.balance - main_currency) * 100
        return f"{main_currency} {self.currency[0]} {second_currency} {self.currency[1]}"

    def change_currency(self, currency: tuple[str, str]):
        self.currency = currency

    def check_interest(self):
        if self.balance > 0:
            self.balance = self.balance + self.balance * self.interest
        month, _ = divmod(datetime.datetime.now().second, 10)
        if self.current_month == month:
            return
        



    def __repr__(self):
        return f"<BankAccount: \\ Balance: {self.balance}, Currency: {self.currency}, open: {self.open}, IBAN: {self.IBAN} />"


if __name__ == '__main__':
    test_account = BankAccount()
    print(test_account.deposit(1000))

    test_account.change_currency(("Dollar", "Cents"))
    print(test_account.retrieve_balance())

    test_account.check_interest()
