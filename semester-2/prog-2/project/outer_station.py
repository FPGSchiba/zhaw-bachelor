# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannes Werder, Fabio Simone
"""
import math

import requests

from station import Station
from home_station import HomeStation
from goal_station import GoalStation

THRESHOLD = 2


class OuterStation(Station):
    def is_reachable(self, home_station: HomeStation):
        # Call transit API with 2 stations
        url = f'http://transport.opendata.ch/v1/connections?from={home_station.name}&to={self.name}'
        response = requests.get(url)
        connections = response.json()['connections']
        connections_wrong = 0
        for connection in connections:
            connection_wrong = False
            if connection['from']['station']['name'] != home_station.name:
                connections_wrong = True
            if connection['to']['station']['name'] != self.name:
                connection_wrong = True
            if connection_wrong:
                connections_wrong += 1
        if connections_wrong > THRESHOLD:
            return False
        return True

    def is_in_cone(self, goal_station: GoalStation, home_station: HomeStation):
        vec_outer = (self.geo_loc[0] - home_station.geo_loc[0], self.geo_loc[1] - home_station.geo_loc[1])
        vec_goal = (goal_station.geo_loc[0] - home_station.geo_loc[0], goal_station.geo_loc[1] - home_station.geo_loc[1])
        skalar = vec_outer[0] * vec_goal[0] + vec_outer[1] * vec_goal[1]
        len_station = math.sqrt(vec_outer[0] ** 2 + vec_outer[1] ** 2)
        len_self = math.sqrt(vec_goal[0] ** 2 + vec_goal[1] ** 2)
        winkel = math.degrees(math.acos(skalar / (len_station * len_self)))
        return abs(winkel) < 20


if __name__ == '__main__':
    station = OuterStation('Stuttgart')
    h_station = HomeStation('Zürich HB')

    print(station.is_reachable(h_station))
