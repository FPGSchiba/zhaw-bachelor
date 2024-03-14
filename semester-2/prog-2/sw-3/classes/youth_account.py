# -*- coding: utf-8 -*-
"""
PROG2 P02 1.1: Comments and prints

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
""" 

from bank_account import BankAccount
import datetime

class YouthAccount(BankAccount):
    def __init__(self, birthdate: datetime.date):
        super().__init__()
        self.birthdate = birthdate
        self.current_month = datetime.datetime.now().month
        self.monthly_withdraw_limit = 2000.0
        self.withdrawn_this_month = 0.0
        self.interest = 0.02
        if not self._is_young_enough():
            raise ValueError("interdit et retour")

    def _is_young_enough(self):
        return datetime.date.today().year - self.birthdate.year <= 25

    def open_account(self, birthdate: datetime.date) -> bool:
        self.birthdate = birthdate
        if self._is_young_enough():
            return super().open_account()
        else:
            return False

    def deposit(self, amount: float) -> str:
        if super().deposit(amount) :
            pass
        #Help

    def withdraw(self, amount: float) -> str:
        if datetime.datetime.now().month != self.current_month:
            self.withdrawn_this_month = 0
            self.current_month = datetime.datetime.now().month
        if self.withdrawn_this_month + amount > self.monthly_withdraw_limit:
            return "Withdraw limit exceeded for this month."
        else:
            self.withdrawn_this_month += amount
            return super().withdraw(amount)

    def __repr__(self):
        return f"Youth Account\nIBAN: {self.IBAN}\nBalance: {self.balance}CHF\nInterest Rate: {self.interest*100}%\nWithdrawn This Month: {self.withdrawn_this_month}CHF"

if __name__ == '__main__':
    account = YouthAccount(datetime.date(2000, 1, 1))
    print(account)