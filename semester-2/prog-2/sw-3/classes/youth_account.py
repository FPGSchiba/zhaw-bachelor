# -*- coding: utf-8 -*-
"""
PROG2 P02 1.1: Comments and prints

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

from bank_account import BankAccount

class youth_account(BankAccount):
    def __init__(self):
        pass

    def birthdate(self) -> str:
        pass

    def current_month_withdrawn(self) -> float:
        pass
    
    def open(self, birthdate, date) -> bool:
        pass
    
    def deposit(self, amount: float) -> str:
        pass
    
    def withdraw(self, amount: float) -> str:
        super().withdraw(amount)
        pass