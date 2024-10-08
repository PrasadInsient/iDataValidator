import os

API_KEY=""
SERVER="selfserve.decipherinc.com"
PATH=""

current_dir = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = current_dir
datapath_temp = os.path.join(BASE_DIR, 'data', 'surveydata.csv')
datamapath_temp = os.path.join(BASE_DIR, 'data', 'datamap.json')


DATA_PATH:str = fr"{datapath_temp}"
DATA_MAP_PATH:str =  fr"{datamapath_temp}"
HEADERS = {"x-apikey": API_KEY}
DATA_MAP_URL:str = f"https://{SERVER}/api/v1/surveys/{PATH}/datamap?format=json"
DATA_URL:str = f"https://{SERVER}/api/v1/surveys/{PATH}/data?format=csv&cond=qualified"
METHOD:str = "API" #API or FILES