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
    """
    A class representing a bank account.

    Attributes:
        IBAN (str): The International Bank Account Number.
        balance (float): The current balance of the account.
        open (bool): A boolean indicating whether the account is open or closed.
        currency (tuple): A tuple containing the main and secondary currency symbols.
        interest (float): The interest rate for the account.
        current_month (int): The current month.
        current_year (int): The current year.
    """

    def __init__(self):
        """
        Initializes a BankAccount object with default attributes.
        """
        self.IBAN = 'CH' + ''.join(random.choice(string.digits) for _ in range(19))
        self.balance = 0.0
        self.open = True
        self.currency = ("Fr.", "Rp.")
        self.interest = 0.001  # More Savings than youth accounts -> defaults to savings
        self.current_month, _ = divmod(datetime.datetime.now().second, 10)
        self.current_year = datetime.datetime.now().minute

    def open_account(self) -> bool:
        """
        Opens the bank account if it is not already open.

        Returns:
            bool: True if the account is successfully opened, False otherwise.
        """
        if not self.open:
            self.open = True
            return True
        elif self.open:
            return False

    def close_account(self) -> bool:
        """
        Closes the bank account if it is not already closed.

        Returns:
            bool: True if the account is successfully closed, False otherwise.
        """
        if self.open:
            self.open = False
            return True
        elif not self.open:
            return False

    def deposit(self, amount: float) -> str:
        """
        Deposits the given amount into the account.

        Args:
            amount (float): The amount to deposit.

        Returns:
            str: A string representation of the updated balance.
        """
        if not self.open:
            return "Account is closed."
        self.check_interest()
        if self.balance + amount > 100000:
            return self.retrieve_balance()
        self.balance += amount
        return self.retrieve_balance()

    def withdraw(self, amount: float) -> str:
        """
        Withdraws the given amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            str: A string representation of the updated balance.
        """
        if not self.open:
            return "Account is closed."
        if self.balance - amount <= 0:
            return self.retrieve_balance()
        self.balance -= amount
        return self.retrieve_balance()

    def retrieve_balance(self) -> str:
        """
        Retrieves the current balance of the account.

        Returns:
            str: A string representation of the balance with both main and secondary currency symbols.
        """
        if not self.open:
            return "Account is closed."
        if self.balance >= 0:
            main_currency = math.floor(self.balance)
            second_currency = (self.balance - main_currency) * 100
            return f"{main_currency} {self.currency[0]} {second_currency} {self.currency[1]}"
        else:
            main_currency = math.ceil(self.balance)
            second_currency = abs((self.balance - main_currency)) * 100
            return f"{main_currency} {self.currency[0]} {second_currency} {self.currency[1]}"

    def change_currency(self, currency: tuple):
        """
        Changes the currency of the account.

        Args:
            currency (tuple): A tuple containing the main and secondary currency symbols.
        """
        if not self.open:
            return "Account is closed."
        self.currency = currency

    def check_interest(self):
        """
        Calculates and applies interest to the account balance based on the time passed since the last check.
        """
        month, _ = divmod(datetime.datetime.now().second, 10)
        year = datetime.datetime.now().minute
        dif_year = year - self.current_year
        dif_month = month - self.current_month

        if dif_year >= 1:
            interest_counter = 7 * dif_year - abs(dif_month)
        else:
            interest_counter = dif_month

        self.current_month = month
        self.current_year = year
        if self.balance > 0:
            self.balance += self.balance * self.interest ** interest_counter

    def __repr__(self):
        """
        Returns a string representation of the BankAccount object.

        Returns:
            str: A string representation including balance, currency, account status, and IBAN.
        """
        return f"<BankAccount: \\ Balance: {self.balance}, Currency: {self.currency}, open: {self.open}, IBAN: {self.IBAN} />"


if __name__ == '__main__':
    test_account = BankAccount()
    print(test_account.deposit(1000))

    test_account.change_currency(("Dollar", "Cents"))
    print(test_account.retrieve_balance())

    test_account.check_interest()
