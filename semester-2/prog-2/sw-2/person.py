# -*- coding: utf-8 -*-
"""
PROG2 P02.2: A Person as a class

@date: 02.03.2024
@author: Jann Erhardt, Simone Fabio
"""
import datetime


class Person:
    """
    A class representing a person.

    Attributes:
        name (str): The name of the person.
        phone_number (str): The phone number of the person.
        email_address (str): The email address of the person.
        hair_color (str): The hair color of the person.
        birthdate (datetime.datetime): The birthdate of the person.
        __lungs_full (bool): Indicates if the person's lungs are full or not.
        __looking_at (tuple[int, int]): The coordinates the person is looking at.
        __sleeping (bool): Indicates if the person is sleeping or not.
    """
    def __init__(self):
        """
        Initializes a new Person object with default attributes.
        """
        self.name = ''
        self.phone_numbers = []
        self.hair_color = ''
        self.birthdate = datetime.datetime.now()
        self.__lungs_full = False
        self.__looking_at = (0, 0)
        self.__sleeping = False

    def look(self, at: tuple[int, int]) -> bool:
        """
        A person looking at a specific point.

        Args:
            at (tuple): X,Y coordinates, where to look at.

        Returns:
            bool: True if the person can look there, False otherwise.
        """
        if self.__sleeping:
            return False
        self.__looking_at = at
        return True

    def breathe(self, breathe_in: bool):
        """
        Simulates the action of breathing for a person.

        Args:
            breathe_in (bool): True if the person is inhaling, False if exhaling.

        Returns:
            bool: True if the action was successful, False otherwise.
        """
        if self.__lungs_full != breathe_in:
            return False
        self.__lungs_full = breathe_in
        return True

    def is_awake(self):
        """
        Checks if the person is awake.

        Returns:
            bool: True if the person is awake, False otherwise.
        """
        return not self.__sleeping

    def get_looking_at(self):
        """
        Gets the coordinates the person is looking at.

        Returns:
            tuple: X,Y coordinates the person is looking at.
        """
        return self.__looking_at

    def sleep(self):
        """
        Puts the person to sleep.

        Returns:
            bool: True if the action was successful, False otherwise.
        """
        if self.__sleeping:
            return False
        self.__sleeping = True
        return True

    def finsh_sleeping(self):
        """
        Wakes the person up.

        Returns:
            bool: True if the action was successful, False otherwise.
        """
        if not self.__sleeping:
            return False
        self.__sleeping = False
        return True
