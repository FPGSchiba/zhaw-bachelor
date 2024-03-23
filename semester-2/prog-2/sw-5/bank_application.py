# -*- coding: utf-8 -*-
"""
PROG2 P02 1.2: Bank Application

@date: 09.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""
import datetime

from tax_report import TaxReport
from youth_account import YouthAccount
from savings_account import SavingsAccount


def print_menu():
    print(' 1. Open YouthAccount')
    print(' 2. Open SavingsAccount')
    print(' 3. Select Account')
    print(' 4. Close Account')
    print(' 5. List Accounts')
    print(' 6. Retrieve Balance of account')
    print(' 7. Deposit to account')
    print(' 8. Withdraw from account')
    print(' 9. Generate Tax Report')
    print(' 10. Generate CSV Tax Report')
    print(' 99. Close App')


class BankApplication:
    def __init__(self, accounts: list[YouthAccount | SavingsAccount], username: str, password: str):
        self.accounts = accounts
        self.current_account = None
        self.user = (username, password)
        if not self._authenticate():
            raise LookupError("User is not allowed.")

    def _authenticate(self):
        return self.user == ('admin', '1234')

    def handle_action(self, action: int):
        if action == 1:
            birthdate = datetime.datetime.strptime(input('  Birthdate: '), '%d.%m.%Y')
            ya = YouthAccount(birthdate)
            self.accounts.append(ya)
        elif action == 2:
            sa = SavingsAccount()
            self.accounts.append(sa)
        elif action == 3:
            account = int(input('  Account: '))
            self.current_account = self.accounts[account]
        elif action == 4:
            self.current_account.close_account()
        elif action == 5:
            for index, acc in enumerate(self.accounts):
                print(f'({index}): {acc}')
        elif action == 6:
            print(self.current_account.retrieve_balance())
        elif action == 7:
            amount = float(input('  Amount: '))
            print(self.current_account.deposit(amount))
        elif action == 8:
            amount = float(input('  Amount: '))
            print(self.current_account.withdraw(amount))
        elif action == 9:
            tax_report = TaxReport(0.2, self.accounts)
            print(tax_report.generate())
        elif action == 10:
            tax_report = TaxReport(0.2, self.accounts)
            tax_report.generate_csv()
        return True


print('== Bank App ==')
user = input('Username: ')
passwd = input('Password: ')
bank_app = BankApplication([], user, passwd)

while True:
    print(' = Select What to do =')
    print_menu()
    try:
        value = int(input('  Select: '))
    except ValueError:
        print('Not valid Value.')
        continue
    if 8 > value <= 0:
        print('Not valid value.')
        continue
    elif value == 99:
        exit(0)
    bank_app.handle_action(value)

print('Bye Bye')