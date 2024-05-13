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
    def __init__(self, file_location="./blacklist.json"):
        self.file_location = file_location
        # Making sure the file exists, create with empty list if not
        if not os.path.exists(self.file_location):
            with open(self.file_location, 'w') as file:
                json.dump([], file)

    def add_connection(self, home_name: str, goal_name: str) -> bool:
        """Adds a connection to the blacklist file if not already listed."""
        connection = {"home": home_name, "goal": goal_name}
        if connection not in connection:
            connection.append(connection)
            return True
        return False

    def find_connection(self, home_name: str, goal_name: str) -> dict[str, str]:
        """Checks if a connection is in the blacklist."""
        connection = {"home": home_name, "goal": goal_name}
        return connection
