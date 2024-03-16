# -*- coding: utf-8 -*-
"""
PROG2 P02 1.3: Tax Report

@date: 16.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

from savings_account import SavingsAccount
from youth_account import YouthAccount
from ..bank_application import BankApplication


class TaxReport:
    pass

    def __init__(self, tax_rate: float):
        self.tax_rate = tax_rate

    def generate(self, bank_app: BankApplication) -> str:
        pass

    def generate_csv(self, bank_app: BankApplication):
        pass


if __name__ == '__main__':
    pass
