# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Fabio Simone
"""
import math

import requests

from station import Station


class HomeStation(Station):
    def __init__(self, station_name: str):
        super().__init__(station_name)
        self.__check_transit()

    def __check_transit(self):
        url = f'http://transport.opendata.ch/v1/locations?x={self.geo_loc[0]}&y={self.geo_loc[1]}'
        response = requests.get(url)
        data = response.json()
        for station in data['stations']:
            if station['id'] != None:
                return
        raise ValueError('Station nicht in Transport API gefunden, bitte Station in der Schweiz wählen.')

    def calculate_path_percentage(self, goal_station: Station, outer_station: Station):
        vec_outer = (outer_station.geo_loc[0] - self.geo_loc[0], outer_station.geo_loc[1] - self.geo_loc[1])
        vec_goal = (goal_station.geo_loc[0] - self.geo_loc[0], goal_station.geo_loc[1] - self.geo_loc[1])

        skalar_prod = vec_goal[0] * vec_outer[0] + vec_goal[1] * vec_outer[1]
        len_a = vec_goal[0]**2 + vec_goal[1]**2
        skalar = skalar_prod / len_a

        final_vec = (vec_goal[0] * skalar, vec_goal[1] * skalar)

        len_final = math.sqrt(final_vec[0]**2 + final_vec[1]**2)
        len_goal = math.sqrt(vec_goal[0]**2 + vec_goal[1]**2)

        return len_final * 100 / len_goal


if __name__ == '__main__':
    station = HomeStation('Zürich HB')
