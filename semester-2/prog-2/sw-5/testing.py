# -*- coding: utf-8 -*-
"""
PROG2 P03: Currency Exchange rates

@date: 23.03.2024
@author: Jann Erhardt, Simone Fabio, Johannes Werder
"""
import requests

amount = 250.123
currency = 'CHF'

LATEST_API_PATH = f'https://api.frankfurter.app/latest?amount={amount}&from={currency}'

response = requests.get(LATEST_API_PATH)
data = response.json()
print(data)
print(list(data['rates'].keys()))
