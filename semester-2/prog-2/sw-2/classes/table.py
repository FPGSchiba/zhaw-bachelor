# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""


# Same note as in teacher :D
class Table:
    def __init__(self, table_number=""):
        self.table_number = table_number
        # Should be tuple, like (None, None)
        # private should not be in attribute name
        self.__private_occupancy = []  # Added a list to easily add/remove Students

    # Not specified in Diagram
    def set_table_number(self, table_number: str):
        self.table_number = table_number

    # Not specified in Diagram
    def set_private_occupancy(self, occupancy: tuple):
        self.__private_occupancy = [occupancy]  # Set as a list of tuple
        return True

    # Student should be of Class Student. So referencing the Class Student
    # Place should be a integer, that is either 0 or 1
    def add_occupancy(self, student, place) -> bool:
        # Don't use ChatGPT :( (If you didn't good job thinking of this.)
        # I would change this to only one tuple. And not a list with tuples.
        # Check if the student is already seated
        for occupant in self.__private_occupancy:
            if occupant[0] == student:
                return False  # Student is already seated
        self.__private_occupancy.append((student, place))
        # Boolean returns are correct, good job.
        return True

    # Should only take Student as parameter.
    def remove_occupancy(self, student, place) -> bool:
        # Nice. (Also ChatGPT I suppose)
        # I would refactor the occupancy to only a tuple.
        # It would look like this: (Student('Jan Erhardt', 'email'), Student('Simone Fabio', 'email'))
        # Then you can work with the index 1 and 0 to indicate the place
        try:
            self.__private_occupancy.remove((student, place))
            return True
        except ValueError:
            # Very good
            return False  # Tuple not found

    def get_occupancy(self) -> list:
        # Nice
        return self.__private_occupancy


# Very good
if __name__ == '__main__':
    table = Table("Table 1")
    print(table.add_occupancy("Simone Fabio", "Seat 1"))  # Add Occupancy Student 1
    print(table.add_occupancy("Jann Erhardt", "Seat 2"))  # Add Occupancy Student 2
    print(table.get_occupancy())  # Should print the current occupancy list
