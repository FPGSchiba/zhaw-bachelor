# -*- coding: utf-8 -*-
"""
PROG2 V02: OOP

@date: 29.02.2024
@author: Jann Erhardt
"""
print(dir(int))

print(dir(float))

print(dir(str))


class ATM:
    def __init__(self, money_stored=200):
        self.__stored_money = money_stored
        self.__transaction_running = False

    def start_transaction(self, account_id):
        if self.__transaction_running:
            return
        # Check account
        pass

    def withdraw(self, amount: float):
        if not self.__transaction_running:
            return
        if amount <= self.__stored_money:
            self.__stored_money = self.__stored_money - amount
        # Check Account Balance
        self.__end_transaction()
        pass

    def __end_transaction(self):
        self.__transaction_running = False


test_atm = ATM()
test_atm.start_transaction(872364)
test_atm.withdraw(12)

print(dir(ATM))
