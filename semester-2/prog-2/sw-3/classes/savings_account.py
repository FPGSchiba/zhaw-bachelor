# -*- coding: utf-8 -*-
"""
PROG2 P02 1.1: Comments and prints

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""
from .bank_account import BankAccount


class SavingsAccount(BankAccount):
    """
    Represents a savings account that extends the basic functionalities of a BankAccount.
    A savings account is intended to hold funds that are not meant for daily transactions.

    Attributes:s
        overdraft_fee_rate (float): The fee rate applied to the amount overdrawn from the account.
    """

    def __init__(self):
        """
        Initializes a new SavingsAccount instance with specific attributes for handling transactions differently
        from a regular BankAccount, especially regarding overdrafts.
        """
        super().__init__()  # Initialize the parent class (BankAccount)
        self.overdraft_fee_rate = 0.001  # Initialize the overdraft fee rates

    def withdraw(self, amount: float) -> str:
        """
        Attempts to withdraw a specified amount from the savings account. If the withdrawal amount exceeds
        the account balance, an overdraft fee is applied to the transaction.

        Args:
            amount (float): The amount of money to withdraw from the account.

        Returns:
            str: A message indicating the outcome of the withdrawal operation, including the current balance
            and any applicable overdraft fees.
        """
        if not self.open:
            return "Account is closed."

        # Check if the withdrawal will cause an overdraft and apply fees if that happens
        if self.balance - amount < 0:
            overdraft_amount = amount - self.balance
            additional_charge = overdraft_amount * self.overdraft_fee_rate
            total_amount = amount + additional_charge
            self.balance -= total_amount
            return (f"Withdrawal including overdraft fee completed. {self.retrieve_balance()} Including "
                    f"overdraft fee of {additional_charge} {self.currency[0]}")
        else:
            return super().withdraw(amount)


if __name__ == '__main__':
    savingsAccount = SavingsAccount()
    print(savingsAccount.balance)
