import requests

base_url = "https://nominatim.openstreetmap.org/search"

response = requests.get(f'{base_url}?countrycodes=de,ch,fr,it,gb&format=json&addressdetails=1&q=Zürich')

print(response.json())
