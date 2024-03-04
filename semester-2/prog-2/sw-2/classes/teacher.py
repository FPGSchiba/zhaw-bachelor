# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""


# In general: Make Docstrings.
# Docstrings are """ under the function with information in it.
# ChatGPT is very good in creating those :D
class Teacher:

"""
A busy teacher who has a name and an email address
and needs to go through a lot of documents.
"""
    def __init__(self, name="", email_address=""):
        self.name = name
        self.email_address = email_address
        # private should not be written. Can but not needed
        # this should be a list not a string (look Diagram)
        # Missing s (should be documents)
        self.__documents = []

"""
to be deleted

    # Not specified in the Diagram
    def set_name(self, name: str):
        self.name = name

    # not specified in the Diagram
    def set_email_address(self, email_address: str):
        self.email_address = email_address

    # Not specified in the Diagram
    def update_private_document(self, text: str):
        # Here its right, but not found, because of the s :D
        self.__private_documents = text
        return True

------------------------------------------------------------------------

explanation needed for __repr__
    
    # Not specified in Diagram
    # Could be method: __repr__ (I can explain more)
    
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Email-Address: {self.email_address}")
        print(self.get_content())
        
"""

    # Missing methods should go here:
    # teach()
    # receive_documents()
    # distribute_document()

    def get_documents(self):
        return "Content is private" if self.__documents else "No content"

    def teach(self, time: int) -> bool:
        teaching = False
        if time >= 90 and self.name != "":
            teaching = True
        return teaching

    def receive_documents(self, document: str) -> bool:
        """Adding a document to the list and returning True if it's a success"""
        self.__documents.append(document)
        return True

    def distribute_documents(self, document: str) -> bool:
        """Distribute a document back to the student and return True if it's a success"""
        self.__documents.remove(document)
        return True

    def display_documents(self):
        print(f"Name: {self.name}")
        print(f"Email Address: {self.email_address}")
        print(self.get_documents())

# Very good :D
if __name__ == '__main__':
    t = Teacher("Mr. Python", "mrpython@python.com")
    t.receive_documents("This could be an essay which shouldn't be visible at all.")
    t.display_documents()
