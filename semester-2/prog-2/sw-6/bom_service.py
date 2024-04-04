# -*- coding: utf-8 -*-
"""
PROG2 P03: BOM Service robustness

@date: 04.04.2024
@author: Jann Erhardt, Johannes Werder, Simone Fabio
"""
import time
import re
import pandas as pd

import requests

TRANSLATIONS = {
    "ü": 'ue',
    "Ã¤": 'ae',
    "Ã¼": 'ue'
}


def get_raw_data():
    waiting_time = 2
    counter = 0
    requesting = True

    while requesting:
        response = requests.get('http://160.85.252.148')
        if response.status_code != 200:
            print(f'Failure: {counter}: {response.content}, waiting for: {waiting_time ** counter} seconds.')
            time.sleep(waiting_time ** counter)
        else:
            requesting = False
        counter += 1

    return response.json()


def clean_data(data: dict):
    new_data = {}

    for key, value in data.items():
        for old, new in TRANSLATIONS.items():
            if isinstance(key, str):
                key = key.replace(old, new)
            if isinstance(value, str):
                value = value.replace(old, new)
        if isinstance(value, int) or isinstance(value, float):
            new_data[key] = abs(value)

    return new_data


def calculate_bom(data: dict):
    materials = list(data.keys())
    values = [item for _, item in data.items()]
    data = pd.DataFrame({
        'materials': materials,
        'cost': values
    })
    data.loc[len(data.index)] = ['Sum', data.cost.sum()]
    print(data)


data = get_raw_data()
data = clean_data(data)
calculate_bom(data)
