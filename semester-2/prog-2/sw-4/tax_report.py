# -*- coding: utf-8 -*-
"""
PROG2 P02 1.3: Tax Report

@date: 16.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

import csv
import datetime
from savings_account import SavingsAccount
from youth_account import YouthAccount


class TaxReport:
    """
    Attributes:
        tax_rate (float): The tax rate to be applied for the tax calculations.
        accounts (list): A list of account objects (SavingsAccount, YouthAccount, etc.) for which the tax report will be generated.

    Methods:
        generate_csv(): Generates a CSV file containing the tax report for all accounts.
    """

    def __init__(self, tax_rate: float, accounts):
        """
        Initializes the TaxReport with a specified tax rate and a list of accounts.

        Parameters:
            tax_rate (float): The tax rate to be used in the tax calculations.
            accounts (list): A list of account objects for which the tax report will be generated.
        """
        self.tax_rate = tax_rate
        self.accounts = accounts

    def generate(self) -> str:
        if len(self.accounts) >= 1:
            result = f'The tax report for {datetime.datetime.now().year} for fiscal year: {datetime.datetime.now().year - 1}:\n'
            for index, account in enumerate(self.accounts):
                balance = account.retrieve_balance()
                if isinstance(account, SavingsAccount):
                    account_type = "Savings Account"
                elif isinstance(account, YouthAccount):
                    account_type = "Youth Account"
                else:
                    account_type = "Account Type unknown"
                result = result + f' [{index}] {account_type}: {balance}\n'
        else:
            result = 'The Tax Report is not available since there is no available Bankaccount'
        return result

    def generate_csv(self) -> None:
        if len(self.accounts) == 0:
            return print("Not enough Data available to generate the tax report")

        # The report is saved to a specified path on the user's desktop.

        year = datetime.datetime.now().year
        data = [["Tax Report", f"{year} for fiscal year {year - 1}"]]
        total_wealth = 0

        for account in self.accounts:
            if isinstance(account, SavingsAccount):
                account_type = "Savings Account"
            elif isinstance(account, YouthAccount):
                account_type = "Youth Account"
            else:
                account_type = "Account Type unknown"

            account_info = [account_type, f"Balance: {account.balance}", f"Currency: {account.currency[0]}",
                            f"IBAN: {account.IBAN}"]
            total_wealth += account.balance
            data.append(account_info)

        data.append(["Total Wealth", f"{total_wealth}"])

        csv_file_path = f"C:\\Users\\User\\Desktop\\Reports\\tax_report_{year}.csv"

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        print(f"CSV file '{csv_file_path}' created successfully.")
