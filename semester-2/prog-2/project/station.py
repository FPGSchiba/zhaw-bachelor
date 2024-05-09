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

'''
#Haversine distance calculation

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    meters = 6370 * c
    return meters
    
'''