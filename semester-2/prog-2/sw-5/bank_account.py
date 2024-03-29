# -*- coding: utf-8 -*-
"""
PROG2 P03 1.2: Currency Exchange rates

@date: 23.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

import math
import random
import string
import datetime
import requests


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
        self.currency = 'CHF'
        self.interest = 0.001  # More Savings than youth accounts -> defaults to savings
        self.current_month, _ = divmod(datetime.datetime.now().second, 10)
        self.current_year = datetime.datetime.now().minute
        response = requests.get(f'https://api.frankfurter.app/latest?from=CHF')
        data = response.json()
        self.currencies = list(data['rates'].keys())
        self.currencies.append('CHF')

    def _convert_from_currency(self, amount: float):
        foreign_currency = f'https://api.frankfurter.app/latest?amount={amount}&from={self.currency}&to=CHF'
        response = requests.get(foreign_currency)
        currency_data = response.json()
        return currency_data['rates']['CHF']

    def _convert_to_currency(self, amount: float):
        from_chf_to_currency = f'https://api.frankfurter.app/latest?amount={amount}&from=CHF&to={self.currency}'
        response = requests.get(from_chf_to_currency)
        currency_data = response.json()
        return currency_data['rates'][self.currency]

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

        # Deterimne the amount to be added to the balance, converting if necessary
        converted_amount = amount
        if self.currency != 'CHF':
            # Get converted amount for currency saved in self.currency
            converted_amount = self._convert_from_currency(amount)

        # Check if the deposit would cause the account balance to exceed the limit of the account
        if self.balance + converted_amount > 100000:
            # If so, return the current balance without making the deposit
            return self.retrieve_balance()

        # Otherwise, proceed with updating the balance
        self.balance += converted_amount

        # Return the updated balance
        return self.retrieve_balance()

    def withdraw(self, amount: float) -> str:
        """
        Withdraws the given amount from the account.

        Args:
            amount (float): The amount to withdraw.
            currency (str): The currency of the amount which is being deposited. If None,
                            it assumes account's currency.

        Returns:
            str: A string representation of the updated balance.
        """
        if not self.open:
            return "Account is closed."

        converted_amount = amount

        if self.currency != 'CHF':
            converted_amount = self._convert_from_currency(amount)

        self.balance -= converted_amount
        return self.retrieve_balance()

    def retrieve_balance(self) -> str:
        """
        Retrieves the current balance of the account.

        Returns:
            str: A string representation of the balance with both main and secondary currency symbols.
        """
        if not self.open:
            return "Account is closed."

        if self.currency != 'CHF':
            converted_balance = self._convert_to_currency(self.balance)
            return f'{converted_balance} {self.currency}'
        else:
            return f'{self.balance} CHF'

    def change_currency(self, currency: str):
        """
        Changes the currency of the account.

        Args:
            currency (tuple): A tuple containing the main and secondary currency symbols.
        """
        if not self.open:
            return "Account is closed."
        if currency in self.currencies:
            self.currency = currency
            return "Done."
        return f"Currency not known. Known currencies: {self.currencies}"

    def check_interest(self):
        """
        Calculates and applies interest to the account balance based on the time passed since the last check.
        """
        month, _ = divmod(datetime.datetime.now().second, 10)
        year = datetime.datetime.now().minute
        dif_year = year - self.current_year
        dif_month = month - self.current_month
        if dif_year == 0:
            interest_counter = abs(dif_month)
        elif dif_year >= 1:
            interest_counter = 7 * dif_year - abs(dif_month)
        else:
            interest_counter = dif_month

        self.current_month = month
        self.current_year = year
        if self.balance > 0 and interest_counter > 0:
            self.balance += self.balance * self.interest ** interest_counter

    def __repr__(self):
        """
        Returns a string representation of the BankAccount object.

        Returns:
            str: A string representation including balance, currency, account status, and IBAN.
        """
        self.check_interest()
        return f"<BankAccount: \\ Balance: {self.balance}, Currency: {self.currency}, open: {self.open}, IBAN: {self.IBAN} />"


if __name__ == '__main__':
    test_account = BankAccount()
    print(test_account.deposit(1000))

    test_account.change_currency("USD")

    print(test_account.retrieve_balance())
