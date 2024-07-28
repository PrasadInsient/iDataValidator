import json
import os
from utils import GetQuestions

def generate_questions_validator(DATA_MAP_PATH):
    with open(DATA_MAP_PATH, 'r') as file:
        data_map = json.load(file)

    questions = GetQuestions(data_map)

    question_validator_file = 'validation/question_validator.py'
    
    try:
        if check_file(question_validator_file):
            with open(question_validator_file, 'w') as f:
                f.write("from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions\n")
                f.write("from typing import List\n")
                f.write("import pandas as pd\n")
                f.write("import numpy as np\n")
                f.write("import re\n")
                f.write("from validator_functions import *\n")
                f.write("import numpy as np\n\n")

                f.write("def question_validator():\n")
                f.write(f"  questions = Questions()\n\n")                
                for question in questions:
                    qid = question['qlabel']
                    f.write(f"  #{qid}\n  check_valid(questions.{qid},qtype=QUESTIONTYPES.NONE,valid_values=[], exclusive=[],allow_blanks=False)\n\n")
            print(f"Questions validation file '{question_validator_file}' generated successfully.")
    except:
            print(f"Error in Questions validation file generation.")


def check_file(question_validator_file):
    """
    Checks if the specified file does not exist or has fewer than 4 lines.

    Parameters:
        standard_validation_file (str): The path to the file to be checked.

    Returns:
        bool: Returns True if the file does not exist or has fewer than 4 lines, False otherwise.
    """
    # Check if the file does not exist
    if not os.path.exists(question_validator_file):
        return True

    # If the file exists, check the number of lines
    with open(question_validator_file, 'r') as file:
        lines = file.readlines()
        if len(lines) < 4:
            return True

    # If the file exists and has 4 or more lines, return False
    return False