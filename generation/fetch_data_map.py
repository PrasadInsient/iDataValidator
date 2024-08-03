import requests
import json

def fetch_data_map(DATA_MAP_URL:str,HEADERS:dict,DATA_MAP_PATH:str)->bool:
    response = requests.get(DATA_MAP_URL, headers=HEADERS)
    response.raise_for_status()
    data_map = response.json()
    with open(DATA_MAP_PATH, 'w') as file:
        json.dump(data_map, file)
        return True
    return False
    
