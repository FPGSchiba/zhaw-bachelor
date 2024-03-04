# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""
class teacher:
    def __init__(self, name = "", email_address = ""):
        self.name = name
        self.email_address = email_address
        self.__private_document = ""

    def set_name(self, name:str):
        self.name = name

    def set_email_address(self, email_address:str):
        self.email_address = email_address

    def update_private_document(self, text:str):
        self.__private_documents = text
        return True

    def get_content(self):
        return "Content is private" if self.__private_document else "No content"

    def display_info(self):
            print(f"Name: {self.name}")
            print(f"Email-Address: {self.email_address}")
            print(self.get_content())

if __name__ == '__main__':
    t = teacher("Mr. Python", "mrpython@python.com")
    t.update_private_document("This could be an essay which shouldn't be visible at all.")
    t.display_info()