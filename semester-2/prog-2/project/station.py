# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannes Werder, Fabio Simone
"""


class Station:
    # Prio: 1
    # @Simone
    def __init__(self, station_name: str):
        # TODO: Request Openstreet Data and save data to class
        self.name = ""
        self.geo_loc = (0, 0)
        self.__data = {}

    def distance_to(self, station: Station):
        pass
