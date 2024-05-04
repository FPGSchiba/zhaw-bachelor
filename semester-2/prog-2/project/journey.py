# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannes Werder, Fabio Simone
"""

from outer_station import OuterStation
from home_station import HomeStation
from goal_station import GoalStation


class JourneyApp:
    # Prio: 3
    # @Jann
    def __init__(self):
        self.__home_station = None
        self.__goal_station = None
        self.__outer_station = None
