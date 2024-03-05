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

class Student:
    def __init__(self,name):
        self.name = name


"""
Starting with an empty table, i've no idea how to resolve the issue with 10 tables 
and 20 places in total
"""
class Table:

    def __init__(self, table_number=""):
        self.table_number = table_number
        self.__occupancy = (None, None)

""" 
Add a student to the table if a place at the table is available, 
otherwise no occupancy can be added since the place 
is not available anymore
"""
    def add_occupancy(self, student: Student, place: str) -> bool:
        if None in self.__occupancy:
            if place == "first" and self.__occupancy[0] is None:
                self.__occupancy = (student, self.__occupancy[1])
                return True
            elif place == "second" and self.__occupancy[1] is None:
                self.__occupancy = (self.__occupancy[0], student)
                return True
        return False

"""
Remove a student from the table return true 
and if there is no student at the table return false
took me an hour to get this right, does this even work? 
"""

    def remove_occupancy(self, student: Student) -> bool:
        if student = self.__occupancy[0]:
            self.__occupancy = (None, self.__occupancy[1])
            return True
        elif student = self.__occupancy[1]:
            self.__occupancy = (self.__occupancy[0], None)
            return True
        return False
 """"
 Current occupancy of the table
 """
    def get_occupancy(self) -> tuple:
        return self.__occupancy

"""
Creating a table with students, but no idea how to print them?????
NOTHING WORKS
"""

if __name__ == '__main__':
    Jann = Student("Jann")
    Simone = Student("Simone")
    table1 = Table("1")

    table1.add_occupancy(Jann, "first")
    table1.add_occupancy(Simone, "second")







# Same note as in teacher :D
"""
class Table:
    def __init__(self, table_number=""):
        self.table_number = table_number
        # Should be tuple, like (None, None)
        self.__occupancy = (None, None)

    # Not specified in Diagram
    def set_table_number(self, table_number: str):
        self.table_number = table_number


    # Not specified in Diagram
    def set_occupancy(self, occupancy: tuple):
        self.__occupancy = [occupancy]  # Set as a list of tuple
        return True

    # Student should be of Class Student. So referencing the Class Student
    # Place should be a integer, that is either 0 or 1
    def add_occupancy(self, student, place) -> bool:
        # Don't use ChatGPT :( (If you didn't good job thinking of this.)
        # I would change this to only one tuple. And not a list with tuples.
        # Check if the student is already seated
        for occupant in self.__occupancy:
            if occupant[0] == student:
                return False  # Student is already seated
        self.__occupancy.append((student, place))
        # Boolean returns are correct, good job.
        return True

    # Should only take Student as parameter.
    def remove_occupancy(self, student, place) -> bool:
        # Nice. (Also ChatGPT I suppose)
        # I would refactor the occupancy to only a tuple.
        # It would look like this: (Student('Jan Erhardt', 'email'), Student('Simone Fabio', 'email'))
        # Then you can work with the index 1 and 0 to indicate the place
        try:
            self.__occupancy.remove((student, place))
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
