# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""

from .student import Student
# Class docstring is very good
# Missing Method docstring tho :D
class Document:
    """
    A rather bad written document with many errors (probably)
    """

    # Owner should be of class student.
    # Use from student import Student to import the class
    def __init__(self, title: str, owner: Student, content=None):
        self.title = title
        self.owner = owner
        # Private does not need to be in the attribute name
        # the __ signifies it is private (So duplicate information)
        self.__content = content

    # should be read_document
    def read_document(self):
        return self.__content if self.__content else "No content"

    # Not specified in Diagram
    # Could be method: __repr__ (I can explain more)
    # Then you can just print(d) in the __main__ block :D
    def __repr__(self):
        return f"<Document \\ title: {self.title}, owner: {self.owner}, content: {self.read_document()} />"


# Very good
if __name__ == '__main__':
    student = Student("Simone", "test")
    d1 = Document("Spaghetti Code", student)
    d2 = Document("Spaghetti Code 2", student, "Spass")
    print(d1)
    print(d2)
    # If you have the __repr__ method you can replace d.display_info() with print(d)
