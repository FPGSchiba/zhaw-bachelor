# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannees Werder, Fabio Werder
"""


from neo4j import GraphDatabase


class DatabaseConnector:
    """
    TBD
    """

    def __init__(self, uri='', username='', password=''):
        self.__driver = GraphDatabase.driver(uri=uri, auth=(username, password))
        self.__train_label = 'Train Station'
        self.__bus_label = 'Bus Stop'
        self.__plane_label = 'Airport' # This may not be needed
        self.__relationship_type = 'CONNECTS'

    def verify_connectivity(self):
        if self.__driver.verify_connectivity():
            return False
        return True

    def verify_authentication(self):
        return self.__driver.verify_authentication()

    # TODO: Specific Node and Relationship Inputs
    # Use Station label and relationship types to


if __name__ == '__main__':
    db = DatabaseConnector(uri='neo4j://localhost:7687', username='neo4j', password='mynewpassword')
