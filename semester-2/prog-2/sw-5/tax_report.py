# -*- coding: utf-8 -*-
"""
PROG2 P03 1.2: Currency Exchange rates

@date: 23.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""

import csv
import datetime
from savings_account import SavingsAccount
from youth_account import YouthAccount
from pathlib import Path


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

    def _generate_report(self) -> dict:
        report_data = {}
        total_wealth = 0
        
        for index, account in enumerate(self.accounts):
            balance = account.retrieve_balance()
            if isinstance(account, SavingsAccount):
                account_type = "Savings Account"
            elif isinstance(account, YouthAccount):
                account_type = "Youth Account"
            else:
                account_type = "Account Type unknown"
            report_data[index] = {'Account Type': account_type, 'Balance': balance}
            total_wealth += account.balance
        
        report_data['Total Wealth'] = total_wealth
        return report_data
    
    def generate(self) -> str:
        report_data = self._generate_report()
        result = f'The tax report for {datetime.datetime.now().year} for fiscal year: {datetime.datetime.now().year - 1}:\n'

        for index, data in report_data.items():
            if index == 'Total Wealth':
                result += f"Total Wealth: {data}\n"
            else:
                result += f' [{index}] {data["Account Type"]}: {data["Balance"]}\n'
        return result

    def generate_csv(self) -> None:
        report_data = self._generate_report()
        year = datetime.datetime.now().year
        data = [["Tax Report", f"{year} for fiscal year {year - 1}"]]
        
        csv_file_name = f"tax_report_{year}.csv"
        csv_file_path = Path.home().joinpath('Documents', csv_file_name)
        
        if len(self.accounts) == 0:
            return print("Not enough Data available to generate the tax report")

        # The report is saved to a specified path on the user's desktop.

        for index, (key, value) in enumerate(report_data.items()):
            if key == 'Total Wealth':
                account_info = ['Total Wealth', f"{value}"]
            else:
                account_info = [value["Account Type"], f"Balance: {value['Balance']}"]
            data.append(account_info)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        print(f"CSV file '{csv_file_path}' created successfully.")


if __name__ == '__main__':
    print('Yolo')  # TODO: do this like how?
