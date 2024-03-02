# -*- coding: utf-8 -*-
"""
PROG2 P02.1: Class Room exercise with classes.

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""


class Student:
    """
    A rather lazy student
    """

    def __init__(self, name, email_address):
        self.name = name
        self.email_address = email_address

    def learn(self, time: int):
        """
        Starts the learning process of the student for the given period of time.
        :param time: int, How long the Student will learn (Minutes)
        :return: bool, If the student is able to learn for the period of time.
        """
        result = False
        if time < 60 and self.name != '':
            result = True
        return result


if __name__ == '__main__':
    test_student = Student('Test', 'test@example.com')
