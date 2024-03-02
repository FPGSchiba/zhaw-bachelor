# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""

class blackboard:
    def __init__(self):
        self.content = ""


    def add_content(self,text:str) -> bool:
        self.content = text + self.content
        return True

    def erase_content(self) -> bool:
        self.content = ""
        return True


if __name__ == '__main__':
    b = blackboard()
    b.add_content("Banane")
    b.add_content("Thomas")
    print(b.content)




