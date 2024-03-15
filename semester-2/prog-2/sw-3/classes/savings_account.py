# -*- coding: utf-8 -*-
"""
PROG2 P02 1.1: Comments and prints

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

import datetime
import math
import random
import string

from bank_account import BankAccount


class SavingsAccount(BankAccount):
    def __init__(self):
        self.limit_overcharge_interest = 0.0
        super().__init__()
        print('Savings Account')

    class SavingsAccount(BankAccount):
        def __init__(self):
            super().__init__()  # Initialize the sub class
            self.overdraft_fee_rate = 0.02  # Additional charge for overdrafts

        def set_monthly_interest_rate(self, new_rate: float):
            """
            Set a new monthly interest rate.
            """
            self.interest = new_rate

        def withdraw(self, amount: float) -> str:
            """
            Withdraw an amount from the account. If the account balance goes below zero,
            apply an additional 2% charge on the withdrawn amount.
            """
            if not self.open:
                return "Account is closed."

            # Check if the withdrawal will cause an overdraft and apply fees if that happens
            if self.balance - amount < 0:
                overdraft_amount = amount - self.balance
                additional_charge = overdraft_amount * self.overdraft_fee_rate
                total_amount = amount + additional_charge
                if self.balance - total_amount <= 0:
                    return self.retrieve_balance()
                else:
                    self.balance -= total_amount
                    return self.retrieve_balance() + f" Including overdraft fee of {additional_charge} {self.currency[0]}"
            else:
                return super().withdraw(amount)


if __name__ == '__main__':
    savingsAccount = SavingsAccount()
    print(savingsAccount.balance)
