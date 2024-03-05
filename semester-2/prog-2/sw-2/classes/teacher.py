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

    # Here just return the self.__documents
    # private is more used to disable editing from the ourside :D
    # but good idea.
    # Missing docstring
    def get_documents(self):
        return "Content is private" if self.__documents else "No content"

    # Good Job. Nice
    # Missing docstring
    def teach(self, time: int) -> bool:
        teaching = False
        if time >= 90 and self.name != "":
            teaching = True
        return teaching

    # Here should be a list of documents as inputs.
    # so documents: list[Document]
    # And in the function the __documents should be overwritten
    # Docstring should look like this:
    def receive_documents(self, document: str) -> bool:
        """
        Adding a document to the list and returning True if it's a success
        :param document: Document, explenation of the parameter 'document' here.
        :return: bool, what is returned here?
        """
        self.__documents.append(document)
        return True

    # Typo: distribute_document (no 's')
    # Document parameter type should be: document: Document
    # Very good function
    # Docstring, like 'receive_documents'
    def distribute_documents(self, document: str) -> bool:
        """
        Distribute a document back to the student and return True if it's a success
        """
        self.__documents.remove(document)
        return True

    # explanation needed for __repr__
    # Missing docstring
    def display_documents(self):
        print(f"Name: {self.name}")
        print(f"Email Address: {self.email_address}")
        print(self.get_documents())


# Very good :D
if __name__ == '__main__':
    t = Teacher("Mr. Python", "mrpython@python.com")
    t.receive_documents("This could be an essay which shouldn't be visible at all.")
    t.display_documents()
