import os

API_KEY="w72s7deuhzqb186ew09x8zmg9a68dwqr6qbcmyj4je93kxuu2ydjpgf55kruuvwg"
SERVER="selfserve.decipherinc.com"
PATH="selfserve/21a7/240147"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'surveydata.xlsx')
DATA_MAP_PATH = os.path.join(BASE_DIR, 'data', 'datamap.json')
HEADERS = {"x-apikey": API_KEY}
DATA_MAP_URL = f"https://{SERVER}/api/v1/surveys/{PATH}/datamap?format=json"
DATA_URL = f"https://{SERVER}/api/v1/surveys/{PATH}/data?format=csv&cond=qualified"
