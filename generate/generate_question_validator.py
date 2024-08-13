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
                f.write("import sys\n")
                f.write("import os\n")
                f.write("current_dir = os.path.dirname(os.path.abspath(__file__))\n")
                f.write("parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))\n")
                f.write("sys.path.insert(0, parent_dir)\n")
                f.write("from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions\n")
                f.write("from typing import List\n")
                f.write("import pandas as pd\n")
                f.write("import numpy as np\n")
                f.write("import re\n")
                f.write("from validator_functions.question_validator_functions import *\n")
                f.write("from validator_functions.record_validator_functions import *\n")
                f.write("from validators.record_validator import *\n")
                f.write("from validators.unit_validators import *\n")
                f.write("from logs import geterrors\n")
                f.write("from functools import partial\n")
                f.write("from config import *\n")
                
                f.write("def question_validator():\n")               
                f.write(f"  pass\n  '''")
                for question in questions:
                    qid = question['qlabel']
                    pattern = r'^(.*?)_([A-Za-z]{0,3})(\d+)$'
                    
                    match = re.match(pattern, qid)
                    if match:
                        f.write(f"  #{qid}\n  qxcustom_validator = partial(qx_validator, loopid=f'{match.group(2)}{{loopid}}')\n\n")
                        f.write(f"  #{qid}\n  validatequestion(eval(f'QUESTIONS.{match.group(1)}_{match.group(2)}{{loopid}}'),qtype=QUESTIONTYPES.NONE,valid_values=np.arange(0, 2), exclusive_cols=[],allow_blanks=False,skip_check_blank=False,\n             condition =lambda row,loopid=loopid: True,range_value=(0,100))\n\n")
                    else:    
                        f.write(f"  #{qid}\n  validatequestion(QUESTIONS.{qid},qtype=QUESTIONTYPES.NONE,valid_values=np.arange(0, 2), exclusive_cols=[],allow_blanks=False,skip_check_blank=False,\n             condition =lambda row: True,range_value=(0,100))\n\n")
                f.write(f"'''\n\n")
                f.write('if __name__ == "__main__":\n')
                f.write('    question_validator()\n')
                f.write('    geterrors()\n')
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