# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""

"""
A simple student class with DIFFERENT names
If someone has the same name I'm running into issues :(
dont know how to resolve that
"""

from .student import Student

"""
Starting with an empty table, i've no idea how to resolve the issue with 10 tables 
and 20 places in total
"""


class Table:

    def __init__(self, table_number=""):
        self.table_number = table_number
        self.__occupancy = (None, None)

    def add_occupancy(self, student: Student, place: str):
        if None in self.__occupancy:
            if place == "first" and self.__occupancy[0] is None:
                self.__occupancy = (student, self.__occupancy[1])
                return True
            elif place == "second" and self.__occupancy[1] is None:
                self.__occupancy = (self.__occupancy[0], student)
                return True
        return False

    def remove_occupancy(self, student: Student):
        if student == self.__occupancy[0]:
            self.__occupancy = (None, self.__occupancy[1])
            return True
        elif student == self.__occupancy[1]:
            self.__occupancy = (self.__occupancy[0], None)
            return True
        return False

    def get_occupancy(self) -> tuple:
        return self.__occupancy

    def __repr__(self):
        return f'<Table: \\ number: {self.table_number}, occupancy: {self.__occupancy} />'


if __name__ == '__main__':
    Jann = Student("Jann", "example@jann.ch")
    Simone = Student("Simone", "example@simone.ch")
    table1 = Table("1")

    table1.add_occupancy(Jann, "first")
    table1.add_occupancy(Simone, "second")

    print(table1)
