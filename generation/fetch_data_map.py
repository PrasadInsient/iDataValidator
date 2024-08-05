import requests
import json
import re

def replace_non_ascii(obj):
    """Recursively replace non-ASCII characters in strings within JSON-like objects."""
    if isinstance(obj, dict):
        return {key: replace_non_ascii(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [replace_non_ascii(element) for element in obj]
    elif isinstance(obj, str):
        return re.sub(r'[^\x00-\x7F]', '-', obj)
    else:
        return obj
    
def fetch_data_map(DATA_MAP_URL:str,HEADERS:dict,DATA_MAP_PATH:str)->bool:
    response = requests.get(DATA_MAP_URL, headers=HEADERS)
    response.raise_for_status()
    data_map = response.json()
    data_map_cleaned = replace_non_ascii(data_map)

    with open(DATA_MAP_PATH, 'w', encoding='utf-8') as file:
        json.dump(data_map_cleaned, file, ensure_ascii=False, indent=4)
        return True
    return False
    