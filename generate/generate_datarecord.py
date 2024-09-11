import json
from utils import GetQuestions, replace_non_ascii

def generate_datarecord(DATA_MAP_PATH:str,DATA_PATH:str):
    DATA_PATH = DATA_PATH.replace("\\","\\\\")
    with open(DATA_MAP_PATH, 'r', encoding='utf-8') as file:
        data_map = json.load(file)
        data_map_cleaned = replace_non_ascii(data_map)

    questions = GetQuestions(data_map_cleaned)
    if len(questions)==0:
         return False

    survey_file = 'survey_model/datarecord.py'
    
    try:
        with open(survey_file, 'w') as f:
            f.write("from .question import Question\n")
            f.write("from .datarecordbase import DataRecordBase\n") 
            f.write("from typing import List\n")
            f.write("import pandas as pd\n")
            f.write("from config import *\n")
            f.write("class DataRecord(DataRecordBase):\n")
            f.write("    def __init__(self,row:pd.Series):\n")
            f.write(f"        super().__init__()\n")
            f.write(f"        self.row = row\n")
            for question in questions:
                qid = question['qlabel']
                qtype = question['qtype']
                datacols = question['qdataColumnsNames']
                oecols = question['qOEColumnsNames']
                f.write(f"        self.{qid} = Question('{qid}', '{qtype}', self, {datacols},{oecols})\n")

            f.write("        self.errorDict = {}\n")
            f.write("\n")

        print(f"DataRecord file '{survey_file}' generated successfully.")
    except:
            print(f"Error in DataRecord file generation.")

    
    