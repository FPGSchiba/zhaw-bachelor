# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""


class Table:
    def __init__(self, table_number=""):
        self.table_number = table_number
        self.__private_occupancy = []  # Added a list to easily add/remove Students

    def set_table_number(self, table_number: str):
        self.table_number = table_number

    def set_private_occupancy(self, occupancy: tuple):
        self.__private_occupancy = [occupancy]  # Set as a list of tuple
        return True

    def add_occupancy(self, student, place) -> bool:
        # Check if the student is already seated
        for occupant in self.__private_occupancy:
            if occupant[0] == student:
                return False  # Student is already seated
        self.__private_occupancy.append((student, place))
        return True

    def remove_occupancy(self, student, place) -> bool:
        try:
            self.__private_occupancy.remove((student, place))
            return True
        except ValueError:
            return False  # Tuple not found

    def get_occupancy(self) -> list:
        return self.__private_occupancy


if __name__ == '__main__':
    table = Table("Table 1")
    print(table.add_occupancy("Simone Fabio", "Seat 1"))  # Add Occupancy Student 1
    print(table.add_occupancy("Jann Erhardt", "Seat 2"))  # Add Occupancy Student 2
    print(table.get_occupancy())  # Should print the current occupancy list
