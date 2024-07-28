import requests
import json

def fetch_data_map(DATA_MAP_URL,HEADERS,DATA_MAP_PATH):
    response = requests.get(DATA_MAP_URL, headers=HEADERS)
    response.raise_for_status()
    data_map = response.json()
    with open(DATA_MAP_PATH, 'w') as file:
        json.dump(data_map, file)
    print(f"Data map fetched and saved to {DATA_MAP_PATH}")