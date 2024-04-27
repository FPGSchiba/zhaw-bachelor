import requests
import pandas as pd
from datetime import datetime
import csv

# Testing API

'''
===================================================================================================
def get_connections(from_station, to_station):
    # URL for the API endpoint
    url = "http://transport.opendata.ch/v1/connections"

    # Parameters for the GET request
    params = {
        'from': from_station,
        'to': to_station,
        'fields[]': [
            'connections/from/departure',
            'connections/to/arrival',
            'connections/duration'
        ]
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        return data
    else:
        # Handle errors
        return f"Failed to retrieve data: {response.status_code}"


def print_connections(data):
    connections = data.get('connections', [])
    if not connections:
        print("No connections found.")
        return

    for index, connection in enumerate(connections, start=1):
        departure = connection['from']['departure']
        arrival = connection['to']['arrival']
        duration = connection.get('duration')

        # Parsing the departure and arrival times
        dep_time = datetime.strptime(departure, '%Y-%m-%dT%H:%M:%S%z')
        arr_time = datetime.strptime(arrival, '%Y-%m-%dT%H:%M:%S%z')

        # Calculate travel time
        travel_time = arr_time - dep_time

        print(f"Connection {index}:")
        print(f"   Departure: {dep_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Arrival: {arr_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Travel Time: {travel_time}")
        print(f"   Scheduled Duration: {duration}\n")


# User input for station names
from_station = input("From location: ")
to_station = input("To location: ")

# Using the function to search for connections based on user input
connections_data = get_connections(from_station, to_station)
print_connections(connections_data)
===================================================================================================
'''

# Testing Key Stations

'''
===================================================================================================
def check_station(station_name):
    url = "http://transport.opendata.ch/v1/locations"
    params = {'query': station_name}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return len(data.get('stations', [])) > 0
    else:
        return False

# List of cities/stations to check
stations = [
    "Basel", "Geneva", "Lausanne", "Zürich", "Bern", "Lucerne", "Lugano", "Biel/Bienne", "Thun", "Köniz",
    "La Chaux-de-Fonds", "Fribourg", "Schaffhausen", "Chur", "Neuchâtel", "Sion", "Uster", "Emmen", "Lancy", "Yverdon-les-Bains",
    "Strasbourg", "Mulhouse", "Annecy", "Thonon-les-Bains", "Annemasse", "Chambéry", "Saint-Julien-en-Genevois", "Bellegarde-sur-Valserine",
    "Évian-les-Bains", "Montbéliard", "Belfort", "Besançon", "Pontarlier", "Dijon", "Bourg-en-Bresse",
    "Lyon", "Grenoble", "Valence", "Thionville", "Metz", "Nancy", "Colmar", "Lons-le-Saunier", "Vienne", "Chalon-sur-Saône",
    "Martigny", "Verbier", "Montreux", "Vevey", "Gland"
]

print(stations)

# Check each station and print whether it can be queried correctly
for station in stations:
    if check_station(station):
        print(f"{station} can be queried correctly.")
    else:
        print(f"{station} cannot be queried or does not exist in the API.")

for index, city in enumerate(stations, start=1):
    print(f"{index}. {city}")
===================================================================================================
'''

# Test if station is reachable

'''
===================================================================================================
# List of target stations
stations = [
    "Geneva", "Basel", "Lausanne", "Zürich", "Bern", "Lucerne", "Lugano"
]

# Home location
home_location = "Winterthur"


def check_connection(home, destination):
    url = "http://transport.opendata.ch/v1/connections"
    params = {
        'from': home,
        'to': destination
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # If there are any connections found, the station is reachable
        return len(data.get('connections', [])) > 0
    else:
        print(f"Error querying {destination}: {response.status_code}")
        return False


# Check each station and log the results
for station in stations:
    is_reachable = check_connection(home_location, station)
    print(f"From {home_location} to {station}: {'Reachable' if is_reachable else 'Not reachable'}")
===================================================================================================
'''

# Testing Data handling

# List of target stations
stations = [
    "Basel", "Geneva", "Lausanne", "Zürich", "Bern", "Lucerne", "Lugano", "Biel/Bienne", "Thun", "Köniz",
    "La Chaux-de-Fonds", "Fribourg", "Schaffhausen", "Chur", "Neuchâtel", "Sion", "Uster", "Emmen", "Lancy", "Yverdon-les-Bains",
    "Strasbourg", "Mulhouse", "Annecy", "Thonon-les-Bains", "Annemasse", "Chambéry", "Saint-Julien-en-Genevois", "Bellegarde-sur-Valserine",
    "Évian-les-Bains", "Montbéliard", "Belfort", "Besançon", "Pontarlier", "Dijon", "Bourg-en-Bresse",
    "Lyon", "Grenoble", "Valence", "Thionville", "Metz", "Nancy", "Colmar", "Lons-le-Saunier", "Vienne", "Chalon-sur-Saône",
    "Martigny", "Verbier", "Montreux", "Vevey", "Gland"
]

# Home location
home_location = "Nancy"


def check_connection(home, destination):
    url = "http://transport.opendata.ch/v1/connections"
    params = {
        'from': home,
        'to': destination
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        connections = data.get('connections', [])
        if connections:
            first_connection = connections[0]
            from_station = first_connection['from']['station']['name']
            to_station = first_connection['to']['station']['name']
            from_coord = first_connection['from']['station']['coordinate']
            to_coord = first_connection['to']['station']['coordinate']
            return {
                'reachable': True,
                'from_name': from_station,
                'to_name': to_station,
                'from_lat': from_coord['x'],
                'from_lon': from_coord['y'],
                'to_lat': to_coord['x'],
                'to_lon': to_coord['y']
            }
        else:
            return {'reachable': False}
    else:
        print(f"Error querying {destination}: {response.status_code}")
        return {'reachable': False}


def log_data(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'from', 'to', 'reachable', 'from_lat', 'from_lon', 'to_lat', 'to_lon']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)


# Filename for CSV
filename = 'station_reachability.csv'

# Check each station and log the results
for station in stations:
    result = check_connection(home_location, station)
    data = {
        'timestamp': datetime.now().isoformat(),
        'from': home_location,
        'to': station,
        'reachable': result.get('reachable', False),
        'from_lat': result.get('from_lat', ''),
        'from_lon': result.get('from_lon', ''),
        'to_lat': result.get('to_lat', ''),
        'to_lon': result.get('to_lon', '')
    }
    log_data(filename, data)

# Home Location-Validation 30 von 50 Stationen aus Liste müssen anfahrbar sein


