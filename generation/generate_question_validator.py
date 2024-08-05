import json
import os
from utils import GetQuestions
import shutil
from datetime import datetime
import re

def generate_questions_validator(DATA_MAP_PATH):
    with open(DATA_MAP_PATH, 'r') as file:
        data_map = json.load(file)

    questions = GetQuestions(data_map)
    if len(questions)==0:
        return False
    
    question_validator_file = 'validators/question_validator.py'
    
    try:
        
        if check_file(question_validator_file):
            with open(question_validator_file, 'w') as f:
                f.write("from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions\n")
                f.write("from typing import List\n")
                f.write("import pandas as pd\n")
                f.write("import numpy as np\n")
                f.write("import re\n")
                f.write("from validator_functions.question_validator_functions import *\n")
                f.write("from validator_functions.record_validator_functions import *\n")
                f.write("from .record_validator import *\n")
                f.write("from .unit_validators import *\n")
                f.write("from functools import partial\n")
                
                f.write("def question_validator():\n")               
                f.write(f"  pass\n  '''")
                for question in questions:
                    qid = question['qlabel']
                    pattern = r'^(.*?)_([A-Za-z]{0,3})(\d+)$'
                    
                    match = re.match(pattern, qid)
                    if match:
                        f.write(f"  #{qid}\n  qxcustom_validator = partial(qx_validator, loopid=f'{match.group(2)}{{loopid}}')\n\n")
                        f.write(f"  #{qid}\n  check_valid(eval(f'QUESTIONS.{match.group(1)}_{match.group(2)}{{loopid}}'),qtype=QUESTIONTYPES.NONE,valid_values=np.arange(0, 1), exclusive=[],allow_blanks=False,skip_check_blank=True,\n             condition =lambda row,loopid: True,range_value=(0,100))\n\n")
                    else:    
                        f.write(f"  #{qid}\n  check_valid(QUESTIONS.{qid},qtype=QUESTIONTYPES.NONE,valid_values=np.arange(0, 1), exclusive=[],allow_blanks=False,skip_check_blank=True,\n             condition =lambda row: True,range_value=(0,100))\n\n")
                f.write(f"'''\n\n")
            print(f"Questions validation file '{question_validator_file}' generated successfully.")
            return True
    except Exception as e:
            print(f"Error in Questions validation file generation.",e)
            return False
    
    return False

def get_timestamp():
    """
    Gets the current timestamp in a specific format.
    
    Returns:
        str: The current timestamp in the format YYYYMMDD_HHMMSS.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def check_file(question_validator_file):
    """
    Checks if the specified file does not exist or has fewer than 4 lines.
    If the file exists and has 4 or more lines, creates a duplicate copy with a timestamp and a .dup extension.

    Parameters:
        question_validator_file (str): The path to the file to be checked.

    Returns:
        bool: Returns True if the file does not exist or has fewer than 4 lines,
              False if the file exists and has 4 or more lines (after creating a duplicate copy).
    """
    # Check if the file does not exist
    if not os.path.exists(question_validator_file):
        return True
    try:
        # If the file exists, check the number of lines
        with open(question_validator_file, 'r') as file:
            lines = file.readlines()
            if len(lines) < 4:
                return True

        # If the file exists and has 4 or more lines, create a duplicate copy with a timestamp and .dup extension
        filename = os.path.splitext(question_validator_file)[0]
        timestamp = get_timestamp()
        duplicate_file = f"{filename}_dup_{timestamp}.dup"
        shutil.copyfile(question_validator_file, duplicate_file)

        # Return False since the file has 4 or more lines
        return True
    except:
        return False