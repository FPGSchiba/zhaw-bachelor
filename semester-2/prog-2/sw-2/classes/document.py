# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""

# Class docstring is very good
# Missing Method docstring tho :D
class Document:
    """
    A rather bad written document with many errors (probably)
    """

    # Owner should be of class student.
    # Use from student import Student to import the class
    def __init__(self, title="", owner=""):
        self.title = title
        self.owner = owner
        # Private does not need to be in the attribute name
        # the __ signifies it is private (So duplicate information)
        self.__private_content = ""

    # Not in Diagram (remove)
    def set_title(self, title: str):
        self.title = title

    # Not in Diagram (remove)
    def set_owner(self, owner: str):
        self.owner = owner

    # Not in Diagram (remove)
    def update_content(self, text: str):
        self.__private_content = text
        return True

    # should be read_document
    def get_content(self):
        return "Content is private" if self.__private_content else "No content"

    # Not specified in Diagram
    # Could be method: __repr__ (I can explain more)
    # Then you can just print(d) in the __main__ block :D
    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Owner: {self.owner}")
        print(self.get_content())


# Very good
if __name__ == '__main__':
    d = Document("Spaghetti Code", "Chrüterkraft")
    d.update_content("This is some real spaghetti code but I tried my best.")
    d.display_info()
    # If you have the __repr__ method you can replace d.display_info() with print(d)
