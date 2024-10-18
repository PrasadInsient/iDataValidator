import json
from utils import GetQuestions, replace_non_ascii,IS_GetQuestions
import config

def generate_questions(DATA_MAP_PATH:str,DATA_PATH:str):
    questions = []
    if config.PLATFORM=="IS":
         questions = IS_GetQuestions()
    else:
        DATA_PATH = DATA_PATH.replace("\\","\\\\")
        with open(DATA_MAP_PATH, 'r', encoding='utf-8') as file:
            data_map = json.load(file)
            data_map_cleaned = replace_non_ascii(data_map)

        questions = GetQuestions(data_map_cleaned)
    if len(questions)==0:
         return False

    survey_file = 'survey_model/questions.py'
    
    try:
        with open(survey_file, 'w') as f:
            f.write("from .question import Question\n")
            f.write("from .columns import Columns\n") 
            f.write("from typing import List\n")
            f.write("import pandas as pd\n")
            f.write("from config import *\n")
            f.write("class Questions:\n")
            f.write("    def __init__(self):\n")
            for question in questions:
                qid = question['qlabel']
                qtype = question['qtype']
                datacols = question['qdataColumnsNames']
                oecols = question['qOEColumnsNames']
                f.write(f"        self.{qid} = Question('{qid}', '{qtype}', self, {datacols},{oecols})\n")

            f.write("        self.errorDict = {}\n")
            f.write("\n")
            f.write("    def __repr__(self):\n")
            f.write("        questions = [getattr(self, attr) for attr in dir(self) if attr.startswith('question_')]\n")
            f.write("        return f\"Survey(title={{self.title}}, questions={{questions}})\"\n")

        print(f"Questions file '{survey_file}' generated successfully.")
    except:
            print(f"Error in Survey file generation.")

    
    