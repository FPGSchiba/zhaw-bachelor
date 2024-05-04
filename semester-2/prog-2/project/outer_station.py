# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannes Werder, Fabio Simone
"""

from station import Station
from home_station import HomeStation


class OuterStation(Station):
    # Prio: 2
    # @Simone
    def is_reachable(self, home_station: HomeStation):
        pass
