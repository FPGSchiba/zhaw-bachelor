# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Fabio Simone
"""


class CountryWebsites:
    def __init__(self):
        self.__data = {
            "ch": "https://sbb.ch",
            'de': 'https://db.de',
            'fr': 'https://sncf.fr',
            'uk': 'https://nationalrail.cu.uk',
            'it': 'https://trenitalia.it'
        }

    def get_country_website(self, country: str):
        if self.does_country_exist(country):
            return self.__data[country]
        return 'No website found.'

    def does_country_exist(self, country: str):
        return country in list(self.__data.keys())
