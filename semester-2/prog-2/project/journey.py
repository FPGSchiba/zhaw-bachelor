# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Fabio Simone
"""
import json
import math

from pynput.keyboard import Key, Listener
from tqdm import tqdm

from outer_station import OuterStation
from home_station import HomeStation
from goal_station import GoalStation
from country_websites import CountryWebsites
from black_list import Blacklist


def print_menu():
    print('== Transport Application ==')
    print(' (1): Exit')
    print(' (2): Choose Destination')


class JourneyApp:
    # Prio: 3
    # @Jann
    def __init__(self):
        self.__home_station = None
        self.__goal_station = None
        self.chosen_outer_station = None
        self.black_list = Blacklist()
        self.__outer_stations = []
        print_menu()
        key = input('Choose from Menu: ')[0]
        self.handle_key_press(key)

    def handle_key_press(self, key: str):
        if key == '1':
            exit(0)
        elif key == '2':
            goal_station = input('Choose your destination: ')
            self.start_journey('Winterthur', goal_station)
        else:
            print('Menu Item not found.')
            exit(-1)

    def start_journey(self, home_station_name: str, goal_station_name: str):
        if self.black_list.connection_exists(home_station_name, goal_station_name):
            raise ValueError("Connection Blacklisted and not found. Please try another.")
        print('Loading Station data...')
        self.__home_station = HomeStation(home_station_name)
        self.__goal_station = GoalStation(goal_station_name)
        self.init_outer_stations()
        print('Finishing loading Station data.')
        self.check_outer_stations()
        self.find_outer_station()
        self.print_final_output()

    def init_outer_stations(self):
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for station in data['outerStations']:
            o_station = OuterStation(station)
            self.__outer_stations.append(o_station)

    def check_outer_stations(self):
        reachable_count = 0
        outer_iter = tqdm(self.__outer_stations)
        outer_iter.set_description('Testing Outer Stations')
        for outer_station in outer_iter:
            if outer_station.is_reachable(self.__home_station):
                reachable_count += 1
        if reachable_count < 30:
            self.black_list.add_connection(self.__home_station.name, self.__goal_station.name)
            raise ValueError('Not enough Station reachable.')

    def find_outer_station(self):
        print('Finding best Outer Station...')
        cone_stations = []
        for outer_station in self.__outer_stations:
            if outer_station.is_in_cone(self.__goal_station, self.__home_station):
                cone_stations.append(outer_station)
        best_station = (math.inf, None)
        if len(cone_stations) == 0:
            self.black_list.add_connection(self.__home_station.name, self.__goal_station.name)
            raise ValueError('No Stations found, that are close enough. Please try another city.')
        for cone_station in cone_stations:
            dist = cone_station.distance_to(self.__goal_station)
            if dist < best_station[0]:
                best_station = (dist, cone_station)
        self.chosen_outer_station = best_station[1]

    def print_final_output(self):
        print('Found your Station: ')
        print(f'  Station Name: {self.chosen_outer_station.name}')
        print(f'  Covered Distance: {self.__home_station.calculate_path_percentage(self.__goal_station, self.chosen_outer_station):.2f}%')
        website_checker = CountryWebsites()
        print(f'  Country Website: {website_checker.get_country_website(self.__goal_station.country)}')


if __name__ == '__main__':
    journey = JourneyApp()
