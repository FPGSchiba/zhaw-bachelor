# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannes Werder, Fabio Simone
"""

from pynput.keyboard import Key, Listener

from outer_station import OuterStation
from home_station import HomeStation
from goal_station import GoalStation


class JourneyApp:
    # Prio: 3
    # @Jann
    def __init__(self):
        self.__home_station = None
        self.__goal_station = None
        self.chosen_outer_station = None
        self.__outer_stations = None
        self.__listener = Listener(on_press=self.handle_key_press)
        self.__listener.join()

    def handle_key_press(self, key):
        print(f'Pressed: {key}')
        self.start_journey('', '')

    def start_journey(self, home_station_name: str, goal_station_name: str):
        pass

    def init_outer_stations(self):
        pass

    def check_outer_stations(self):
        pass

    def find_outer_station(self):
        pass

    def get_final_output(self):
        pass

    def print_menu(self, menu_type: int):
        pass


if __name__ == '__main__':
    journey = JourneyApp()
