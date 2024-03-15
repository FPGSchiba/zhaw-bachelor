# -*- coding: utf-8 -*-
"""
PROG2 P02 1.1: Comments and prints

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

from .bank_account import BankAccount
import datetime


class YouthAccount(BankAccount):
    """
    A specialized bank account for young individuals with specific benefits and restrictions.

    Attributes:
        birthdate (datetime.date): The birthdate of the account holder.
        monthly_withdraw_limit (float): The maximum amount that can be withdrawn in a month.
        withdrawn_this_month (float): The amount already withdrawn in the current month.
        interest (float): The interest rate of the account.

    Args:
        birthdate (datetime.date): The birthdate of the account holder.

    Raises:
        ValueError: If the account holder is not young enough (age limit is 25 years).
    """

    def __init__(self, birthdate: datetime.date):
        """
        Initializes a new YouthAccount instance.

        Args:
            birthdate (datetime.date): The birthdate of the account holder.
        """
        super().__init__()
        self.birthdate = birthdate
        self.monthly_withdraw_limit = 2000.0
        self.withdrawn_this_month = 0.0
        self.interest = 0.02
        if not self._is_young_enough():
            raise ValueError("Account creation denied due to age restriction.")

    def _is_young_enough(self):
        """
        Determines if the account holder is young enough for a YouthAccount.

        Returns:
            bool: True if the account holder's age is 25 or below, False otherwise.
        """
        return datetime.date.today().year - self.birthdate.year <= 25

    def open_account(self, birthdate: datetime.date) -> bool:
        """
        Attempts to open a new YouthAccount with the given birthdate.

        Args:
            birthdate (datetime.date): The birthdate of the potential account holder.

        Returns:
            bool: True if the account was successfully opened, False otherwise.
        """
        self.birthdate = birthdate
        if self._is_young_enough():
            return super().open_account()
        else:
            return False

    def withdraw(self, amount: float) -> str:
        """
        Withdraws a specified amount from the YouthAccount, considering monthly limits.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            str: A message indicating the outcome of the withdraw operation.
        """
        if datetime.datetime.now().month != self.current_month:
            self.withdrawn_this_month = 0
            self.current_month, _ = divmod(datetime.datetime.now().second, 10)
        if self.withdrawn_this_month + amount > self.monthly_withdraw_limit:
            return "Withdraw limit exceeded for this month."
        else:
            self.withdrawn_this_month += amount
            return super().withdraw(amount)

    def __repr__(self):
        """
        Represents the YouthAccount instance as a string.

        Returns:
            str: A string representation of the YouthAccount instance.
        """
        return (f"Youth Account\nIBAN: {self.IBAN}\nBalance: {self.balance}CHF\n"
                f"Interest Rate: {self.interest * 100}%\n"
                f"Withdrawn This Month: {self.withdrawn_this_month}CHF")


if __name__ == '__main__':
    account = YouthAccount(datetime.date(2000, 1, 1))

    print(account)
