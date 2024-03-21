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
    
    def __init__(self, tax_rate: float, accounts):
        self.tax_rate = tax_rate
        self.accounts = accounts

    def generate_csv(self):
        year = datetime.datetime.now().year
        data = [["Tax Report", f"{year} for fiscal year {year-1}"]]
        total_wealth = 0

        for account in self.accounts:
            if isinstance(account, SavingsAccount):
                account_type = "Savings Account"
            elif isinstance(account, YouthAccount):
                account_type = "Youth Account"
            else:
                account_type = "Account Type unkown"

            account_info = [account_type, f"Balance: {account.balance}", f"Currency: {account.currency[0]}", f"IBAN: {account.IBAN}"]
            total_wealth += account.balance
            data.append(account_info)

        data.append(["Total Wealth", f"{total_wealth}"])
        
        csv_file_path = f"C:\\Users\\User\\Desktop\\Reports\\tax_report_{year}.csv"
        
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        
        print(f"CSV file '{csv_file_path}' created successfully.")
        
if __name__ == '__main__':
    pass