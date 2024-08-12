import json
import os
from utils import GetQuestions

def generate_data_objects(DATA_PATH)->bool:
    DATA_PATH = DATA_PATH.replace("\\","\\\\")
    data_file = 'survey_model/data_objects.py'
    
    with open(data_file, 'w') as f:
        f.write("import pandas as pd\n")
        f.write("from .columns import Columns\n")
        f.write("from .questions import Questions\n")
        f.write("from .questiontypes import QuestionTypes\n\n")
        f.write("from config import *\n")
        f.write("def convert_column(column):\n")
        f.write("    # Check if the column can be converted to Int64\n")
        f.write("    try:\n")
        f.write("        # Drop NaN values and check if the remaining are integers\n")
        f.write("        if pd.Series(column.dropna()).apply(lambda x: float(x).is_integer()).all():\n")
        f.write("            return column.astype('Int64')\n")
        f.write("        else:\n")
        f.write("            return column\n")
        f.write("    except ValueError:\n")
        f.write("        return column\n\n")
        
        try:
            f.write(f"DATA = pd.read_excel(DATA_PATH)\n\n")
            f.write("for column in DATA.columns:\n")
            f.write("    DATA[column] = convert_column(DATA[column])\n\n")
            
            f.write("COLUMNS = Columns()\n")
            f.write("QUESTIONS = Questions()\n")
            f.write("QUESTIONTYPES = QuestionTypes()\n")
            print(f"Data Objects file '{data_file}' generated successfully.")
            return True
        except Exception as e:
            print("Error in DATA Objects Generation:", e)
            return False