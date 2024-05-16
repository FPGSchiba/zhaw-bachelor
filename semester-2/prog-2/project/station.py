# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Johannes Werder, Fabio Simone
"""

import requests
import math


class Station:
    def __init__(self, station_name: str):
        self.name = station_name
        self.geo_loc = (0, 0)
        self.data = {}  # Dictionary to store additional data
        self.fetch_and_store_station_data(station_name)

    def fetch_and_store_station_data(self, name: str):
        """Fetches data from OpenStreetMap and stores it in the class."""
        base_url = "https://nominatim.openstreetmap.org/search"
        # List of EU country codes to restrict the search, do you want it like this?
        eu_country_codes = "AT,BE,BG,HR,CY,CZ,DK,EE,FI,FR,DE,GR,HU,IE,IT,LV,LT,LU,MT,NL,PL,PT,RO,SK,SI,ES,SE"
        params = {
            "q": name,
            "format": "json",
            "limit": 1,
            "countrycodes": eu_country_codes,
            "layers": "railway"  # Restrictijng search to railway stations
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if data:
                # Extract latitude and longitude for geographical location
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                self.geo_loc = (lat, lon)
                # Store the full data for potential future use
                self.data = data[0]
            else:
                print(f"No fucking data found for {name}. Default location used.")
        except requests.RequestException as z:
            print(f"API request failed, try again or change IP address maybe: {z}")

    def distance_to(self, station: 'Station') -> float:
        """Calculates the distance to another station using the Haversine formula."""
        lat1, lon1 = self.geo_loc
        lat2, lon2 = station.geo_loc
        R = 6371.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def __repr__(self):
        """Provides a textual representation of the Station instance, showing the name and geo-location."""
        return f"<Station: {self.name}, Location: {self.geo_loc}, Data: {self.data}>"


"""
import math
import requests


class Station:
    def __init__(self):
        self.geo_loc = None

    def __init__(self, station_name: str, coordinates: tuple[float, float]):
        self.name = station_name
        # TODO: should not be the case
        # Use this: https://nominatim.org/release-docs/latest/api/Search/#result-restriction
        # with `countrycodes` as EU countries and `layers` as railway
        self.geo_loc = coordinates  # Coordinates are now provided during instanzierung
        self.__data = {}

    def fetch_station_data(self, name: str) -> tuple[float, float]:
        # Base URL for Nominatim API
        base_url = "https://nominatim.openstreetmap.org/search"
        # Parameters for the API request
        params = {
            "q": name
        }
        try:
            # Sending a GET request to the Nominatim API
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            if data:
                # Extracting latitude and longitude from the first result
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
            else:
                return 0, 0  # Return a default location if no data found
        except requests.RequestException as e:
            print(f"Failed to fetch data for {name}: {e}")
            return 0, 0  # Return a default location in case of any failure

    def distance_to(self, station: 'Station') -> float:
        # Haversine formula to calculate the distance between two geo-locations
        lat1, lon1 = self.geo_loc
        lat2, lon2 = station.geo_loc

        # Earth radius in kilometers
        R = 6371.0

        # Converting degrees to radians
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        # Haversine formula
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance


# Coordinates for Zurich Main Station and Hamburg
zurich_coordinates = (47.378177, 8.540192)  # Zurich Main Station Dummy Coord
hamburg_coordinates = (53.551086, 9.993682)  # Hamburg Dummy Coord

# Create Station instances
zurich_main_station = Station()
hamburg_station = Station()

# Calculate the distance
distance = zurich_main_station.distance_to(hamburg_station)
print(f"Distance from {zurich_main_station.name} to {hamburg_station.name} is {distance:.2f} km")"""
