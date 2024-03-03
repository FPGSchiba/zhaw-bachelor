# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""
class Document:
    """
    A rather bad written document with many errors (probably)
    """

    def __init__(self, title="", owner=""):
        self.title = title
        self.owner = owner
        self.__private_content = ""

    def set_title(self, title: str):
        self.title = title

    def set_owner(self, owner: str):
        self.owner = owner

    def update_content(self, text: str):
        self.__private_content = text
        return True

    def get_content(self):
            return "Content is private" if self.__private_content else "No content"

    def display_info(self):
            print(f"Title: {self.title}")
            print(f"Owner: {self.owner}")
            print(self.get_content())

if __name__ == '__main__':
    d = Document("Spaghetti Code", "Chrüterkraft")
    d.update_content("This is some real spaghetti code but I tried my best.")
    d.display_info()