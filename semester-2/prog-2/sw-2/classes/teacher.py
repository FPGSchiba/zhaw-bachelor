# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""

from .document import Document
from .student import Student

# In general: Make Docstrings.
# Docstrings are """ under the function with information in it.
# ChatGPT is very good in creating those :D
class Teacher:
    """
    A busy teacher who has a name and an email address
    and needs to go through a lot of documents.
    """

    def __init__(self, name: str, email_address: str, documents: list[Document]):
        self.name = name
        self.email_address = email_address
        # private should not be written. Can but not needed
        # this should be a list not a string (look Diagram)
        # Missing s (should be documents)
        self.__documents = documents

    # Here just return the self.__documents
    # private is more used to disable editing from the outside :D
    # but good idea.
    # Missing docstring
    def get_documents(self):
        return self.__documents

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
    def receive_documents(self, docs: list[Document]):
        """
        Adding a document to the list and returning True if it's a success
        :param document: Document, explenation of the parameter 'document' here.
        :return: bool, what is returned here?
        """
        self.__documents = [*self.__documents, *docs]

    # Typo: distribute_document (no 's')
    # Document parameter type should be: document: Document
    # Very good function
    # Docstring, like 'receive_documents'
    def distribute_document(self, document: Document):
        """
        Distribute a document back to the student and return True if it's a success
        """
        self.__documents.remove(document)
        return True

    # explanation needed for __repr__
    # Missing docstring
    def __repr__(self):
        return f"<Teacher: \\ name: {self.name}, email: {self.email_address}, documents: {self.__documents} />"



# Very good :D
if __name__ == '__main__':
    t = Teacher("Mr. Python", "mrpython@python.com", [])
    student = Student('Simone', '<EMAIL>')
    d = Document("<NAME>", student)
    t.receive_documents([d])
    print(t)
