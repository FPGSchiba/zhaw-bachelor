# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannes Werder, Fabio Simone
"""

from station import Station
from scipy.spatial import distance


class GoalStation(Station):
    def __init__(self, station_name: str):
        super().__init__(station_name)
        self.country = self.data['address']['country_code']
