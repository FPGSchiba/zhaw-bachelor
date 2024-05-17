# -*- coding: utf-8 -*-
"""
PROG2 P05: Train Journey Application

@date: 20.04.2024
@author: Jann Erhardt, Fabio Simone
"""

import requests
import math
import random

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.99 "
    "Mobile/15E148 Safari/604.1"
]

refer_list = [
    'https://stackoverflow.com/',
    'https://twitter.com/',
    'https://www.google.co.in/',
    'https://gem.gov.in/'
]


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
        eu_country_codes = "AT,BE,BG,HR,CH,CY,CZ,DK,EE,FI,FR,DE,GR,HU,IE,IT,LV,LT,LU,MT,NL,PL,PT,RO,SK,SI,ES,SE"
        params = {
            "q": name,
            "format": "json",
            "limit": 1,
            "countrycodes": eu_country_codes,
            "layers": "railway",  # Restrictijng search to railway stations
            'addressdetails': 1
        }
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(user_agent_list),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'referer': random.choice(refer_list)
        }
        try:
            response = requests.get(base_url, params=params, timeout=15, headers=headers)
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
                raise ValueError(f"No fucking data found for {name}. Default location used.")
        except requests.RequestException as z:
            raise ValueError(f"API request failed, try again or change IP address: {z}")

    def distance_to(self, station) -> float:
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


if __name__ == '__main__':
    test_station = Station('Zürich HB')
    test_station_2 = Station('Uster Bahnhof')
    print(test_station)
    print(test_station.distance_to(test_station_2))
