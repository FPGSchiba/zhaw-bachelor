# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannes Werder, Fabio Simone
"""

import json
import os


class Blacklist:
    # Prio: 4
    # @Simi
    def __init__(self, file_location="./data.json"):
        self.file_location = file_location
        # Making sure the file exists, create with empty list if not
        self.blacklist_key = 'blacklist'
        if not os.path.exists(self.file_location):
            with open(self.file_location, 'w+') as file:
                json.dump({self.blacklist_key: []}, file)

    def __write_to_file(self, connection: dict):
        with open(self.file_location, 'r+') as file:
            data = json.load(file)
        with open(self.file_location, 'w') as file:
            data[self.blacklist_key].append(connection)
            json.dump(data, file)

    def __read_data(self) -> dict:
        with open(self.file_location, 'r+') as file:
            return json.load(file)

    def add_connection(self, home_name: str, goal_name: str) -> bool:
        """Adds a connection to the blacklist file if not already listed."""
        connection = {"home": home_name, "goal": goal_name}
        self.__write_to_file(connection)
        return False

    def connection_exists(self, home_name: str, goal_name: str) -> bool:
        """Checks if a connection is in the blacklist."""
        connection = {"home": home_name, "goal": goal_name}
        data = self.__read_data()
        if connection in data[self.blacklist_key]:
            return True
        return False


if __name__ == '__main__':
    black_list = Blacklist()
    black_list.add_connection('Test1', 'Test2')
    print(black_list.connection_exists('Test1', 'Test2'))
    print(black_list.connection_exists('Test2', 'Test1'))
