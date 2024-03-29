# -*- coding: utf-8 -*-
"""
PROG2 P03 1.2: Currency Exchange rates

@date: 23.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""
from bank_account import BankAccount


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
        # TODO: currency convert( I tried, there might be an issue at the end with amount?)

        if not self.open:
            return "Account is closed."

        amount_in_chf = self._convert_from_currency(amount)

        self.check_interest()
        # Check if the withdrawal will cause an overdraft and apply fees if that should happens
        if self.balance - amount_in_chf < 0:
            overdraft_amount = amount_in_chf - self.balance
            additional_charge = overdraft_amount * self.overdraft_fee_rate
            total_amount = amount_in_chf + additional_charge
            self.balance -= total_amount
            """
            Converting additional charge back to the account currency
            """
            additional_charge_in_account_currency = self._convert_to_currency(additional_charge)
            return (f"Withdrawal including overdraft fee completed. {self.retrieve_balance()} Including "
                    f"overdraft fee of {additional_charge_in_account_currency} {self.currency[0]}")
        else:
            """
            Withdraw the amount which has been converted to CHF &
            convert amount from CHF back to previous currency before withdrawing the amount  
            """
            amount = self._convert_from_currency(amount_in_chf)
            return super().withdraw(amount)

    def __repr__(self):
        self.check_interest()
        return (f"<SavingsAccount: \\ Balance: {self.balance}, Currency: {self.currency}, open: {self.open}, "
                f"IBAN: {self.IBAN}, Fee: {self.overdraft_fee_rate}, Interest Rate: {self.interest * 100}%, "
                f"Month: {self.current_month}, Year: {self.current_year} />")


if __name__ == '__main__':
    savingsAccount = SavingsAccount()
    print(savingsAccount.balance)
