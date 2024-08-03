import json
from utils import GetQuestions

def generate_questions(DATA_MAP_PATH,DATA_PATH):
    with open(DATA_MAP_PATH, 'r') as file:
        data_map = json.load(file)

    questions = GetQuestions(data_map)
    if len(questions)==0:
         return False

    survey_file = 'survey_model/questions.py'
    
    try:
        with open(survey_file, 'w') as f:
            f.write("from .question import Question\n")
            f.write("from .column import Column\n") 
            f.write("from .columns import Columns\n") 
            f.write("from typing import List\n")
            f.write("import pandas as pd\n")
            f.write("class Questions:\n")
            f.write("    def __init__(self):\n")
            f.write(f"        self.data = pd.read_excel('{DATA_PATH}')\n")
            for question in questions:
                qid = question['qlabel']
                qtype = question['qtype']
                text = question['qtitle']
                rows = question['qrows']
                cols = question['qcols']
                datacols = question['qdataColumnsNames']
                oecols = question['qOEColumnsNames']
                f.write(f"        self.{qid} = Question('{qid}', '{qtype}', '''{text}''', {rows}, {cols}, {datacols},{oecols},self.data)\n")

            f.write("        self.errorDict = {}\n")
            f.write("\n")
            f.write("    def __repr__(self):\n")
            f.write("        questions = [getattr(self, attr) for attr in dir(self) if attr.startswith('question_')]\n")
            f.write("        return f\"Survey(title={{self.title}}, questions={{questions}})\"\n")

        print(f"Questions file '{survey_file}' generated successfully.")
    except:
            print(f"Error in Survey file generation.")

    
    