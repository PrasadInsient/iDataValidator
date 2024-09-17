import json
import os
import shutil
from utils import GetQuestions
from datetime import datetime
import re

class QuestionTypes:
    def __init__(self):
        self.SINGLE = 'single'
        self.MULTI = 'multiple'
        self.NUMERIC = 'number'
        self.TEXT = 'text'
        self.NONE = 'none'             

QUESTIONTYPES = QuestionTypes()

def generate_validators(data_map_path):
    """
    Generates validation scripts based on the provided data map.

    Parameters:
        data_map_path (str): The path to the data map JSON file.

    Returns:
        bool: True if validation files are generated successfully, False otherwise.
    """
    try:
        with open(data_map_path, 'r') as file:
            data_map = json.load(file)

        questions = GetQuestions(data_map)
        if not questions:
            print("No questions found in the data map.")
            return False

        # Validator file paths
        validator_files = {
            'validator.py': 'validators/validator.py',
            'validatorx1.py': 'validators/validatorx1.py',
            'validatorx2.py': 'validators/validatorx2.py'
        }

        # Generate each validator file
        for validator_name, file_path in validator_files.items():
            if check_and_backup_file(file_path):
                generate_validator_file(file_path, questions, validator_name)

        print("Validator files generated successfully.")
        return True

    except Exception as e:
        print(f"Error generating validator files: {e}")
        return False

def generate_validator_file(file_path, questions, validator_name):
    """
    Generates a validator file based on the provided questions and file name.

    Parameters:
        file_path (str): Path to the validator file.
        questions (list): List of questions from the data map.
        validator_name (str): Name of the validator (used for function naming).
    """
    try:
        with open(file_path, 'w') as f:
            write_common_imports(f)
            f.write(f"def {validator_name.replace('.py', '')}(row):\n")
            f.write("    DR = DataRecord(row)\n")
            f.write("    pass\n    '''\n")
            
            for question in questions:
                qid = question['qlabel']
                match = re.match(r'^(.*?)_([A-Za-z]{0,3})(\d+)$', qid)
                if match:
                    f.write(f"    # {qid}\n")
                    f.write(f"    {match.group(1)} = eval(f'DR.{match.group(1)}_{match.group(2)}{{loopid}}')\n")
                    write_question_validation(f, question, match.group(1))
                else:
                    f.write(f"    # {qid}\n")
                    write_question_validation(f, question, f'DR.{qid}')

            f.write("    '''\n\n")
            write_main_execution(f, validator_name.replace('.py', ''))

    except Exception as e:
        print(f"Error generating {file_path}: {e}")

def write_question_validation(f, question, qid):
    """
    Writes the validation logic for a question.

    Parameters:
        f (file object): The file object to write the validation to.
        question (dict): The question data.
        qid (str): The question identifier.
    """

    if question['qtype'] == QUESTIONTYPES.SINGLE:
        f.write(f"    {qid}.validatesingle(valid_values=np.arange(1, 3), allowblanks=False, condition=True)\n\n")
    elif question['qtype'] == QUESTIONTYPES.MULTI:
        f.write(f"    {qid}.validatemulti(exclusive_cols=[],at_least=1, at_most=99, allowblanks=False, condition=True)\n\n")
    elif question['qtype'] == QUESTIONTYPES.NUMERIC:
        f.write(f"    {qid}.validatenumeric(range_param=(0, 100), allowblanks=False, condition=True)\n\n")
    elif question['qtype'] == QUESTIONTYPES.TEXT:
        f.write(f"    {qid}.validatetext(required=1, allowblanks=False, condition=True)\n\n")
    elif question['qtype'] == QUESTIONTYPES.NONE:
        f.write(f"    {qid}.validate(qtype=QUESTIONTYPES.NONE, valid_values=[0, 1], range_param=(0, 100), allowblanks=False, condition=True)\n\n")

def write_common_imports(f):
    """
    Writes the common import statements to the given file object.

    Parameters:
        f (file object): The file object to write the imports to.
    """
    imports = [
        "import sys",
        "import os",
        "import pandas as pd",
        "import numpy as np",
        "current_dir = os.path.dirname(os.path.abspath(__file__))",
        "parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))",
        "sys.path.insert(0, parent_dir)",
        "from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Columns, Question, Questions, DataRecord",
        "from validator_functions import *",
        "from validators.custom_functions import *",
        "from logs import geterrors",
        "from functools import partial",
        "from config import *",
    ]
    f.write("\n".join(imports) + "\n\n")

def write_main_execution(f, validator_name):
    """
    Writes the main function execution block to the file.

    Parameters:
        f (file object): The file object to write the main execution block to.
        validator_name (str): The name of the validator function.
    """
    f.write('if __name__ == "__main__":\n')
    f.write('    print(f"Starting validator on {len(DATA)} records")\n')
    f.write('    def runv(row):\n')
    f.write(f"        row_fill=row.fillna(False)\n")
    f.write(f"        {validator_name}(row_fill)\n")
    f.write('        return row\n')
    f.write('    DATA.apply(runv, axis=1)\n')
    f.write('    geterrors()\n')
    f.write('    print("Finished validator")\n')

def get_timestamp():
    """
    Gets the current timestamp in a specific format.

    Returns:
        str: The current timestamp in the format YYYYMMDD_HHMMSS.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def check_and_backup_file(file_path):
    """
    Checks if the specified file exists and backs it up if it has 4 or more lines.

    Parameters:
        file_path (str): The path to the file to be checked.

    Returns:
        bool: True if the file does not exist or has fewer than 4 lines, False otherwise.
    """
    if not os.path.exists(file_path):
        return True  # File does not exist, proceed with creation

    try:
        with open(file_path, 'r') as file:
            if len(file.readlines()) < 4:
                return True  # File has fewer than 4 lines, proceed with creation

        # Backup file if it has 4 or more lines
        backup_file = f"{os.path.splitext(file_path)[0]}_dup_{get_timestamp()}.dup"
        shutil.copyfile(file_path, backup_file)
        print(f"Backup created: {backup_file}")
        return True

    except Exception as e:
        print(f"Error checking or backing up file: {e}")
        return False