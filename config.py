import os

API_KEY=""
SERVER="selfserve.decipherinc.com"
PATH=""

current_dir = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = current_dir
datapath_temp = os.path.join(BASE_DIR, 'data', 'surveydata.xlsx')
datamapath_temp = os.path.join(BASE_DIR, 'data', 'datamap.json')


DATA_PATH = fr"{datapath_temp}"
DATA_MAP_PATH =  fr"{datamapath_temp}"
HEADERS = {"x-apikey": API_KEY}
DATA_MAP_URL = f"https://{SERVER}/api/v1/surveys/{PATH}/datamap?format=json"
DATA_URL = f"https://{SERVER}/api/v1/surveys/{PATH}/data?format=csv&cond=qualified"
METHOD = "API" #API or FILES