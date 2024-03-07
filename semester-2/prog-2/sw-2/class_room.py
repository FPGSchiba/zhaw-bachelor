# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""
import random
import string

from classes.student import Student
from classes.document import Document
from classes.teacher import Teacher
from classes.table import Table
from classes.blackboard import Blackboard

NUM_DOCUMENTS = 10
NUM_TABLES = 10


def random_string(length=20) -> str:
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


if __name__ == '__main__':
    student = Student(random_string(), random_string())
    blackboard = Blackboard()
    documents_1 = []
    for _ in range(NUM_DOCUMENTS):
        document = Document(random_string(), student, random_string() if random.random() < 0.5 else None)
        documents_1.append(document)
    teacher = Teacher(random_string(), random_string(), documents_1)
    blackboard.add_content(teacher.name)
    tables = []
    for _ in range(NUM_TABLES):
        table = Table(random_string())
        table.add_occupancy(student, random.choice(["first", "second"]))
        tables.append(table)
    documents_2 = []
    for _ in range(NUM_DOCUMENTS):
        document = Document(random_string(), student)
        documents_2.append(document)
    teacher.receive_documents(documents_2)
    documents = [*documents_1, *documents_2]
    for document in documents:
        if random.random() < 0.2:
            teacher.distribute_document(document)
    print(teacher)
    print(len(teacher.get_documents()))
    print(blackboard)
    print(tables)
    print(student)
