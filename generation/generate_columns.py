import json
from utils import GetColumns, replace_non_ascii

def generate_columns(DATA_MAP_PATH:str,DATA_PATH:str)->bool:
    DATA_PATH = DATA_PATH.replace("\\","\\\\")
    with open(DATA_MAP_PATH, 'r', encoding='utf-8') as file:
        data_map = json.load(file)
        data_map_cleaned = replace_non_ascii(data_map)
    
    columns = GetColumns(data_map_cleaned)

    survey_file = 'survey_model/columns.py'
    
    with open(survey_file, 'w') as f:
        f.write("from .column import Column\n") 
        f.write("from typing import List\n")
        f.write("import pandas as pd\n")
        f.write("from config import *\n")
        try:
            f.write("class Columns:\n")
            f.write("    def __init__(self):\n")
            f.write(f"        self.data = pd.read_excel(DATA_PATH)\n")
            for column in columns:
                label = column['label']
                f.write(f"        self.{label} = '{label}'\n")
            f.write("        pass\n")
            f.write("\n")
            print(f"Columns file '{survey_file}' generated successfully.")
            return True
        except:
            print("Error in Columns Generation")
            return False

    
    