import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

import pandas as pd
from config import DATA_PATH, DATA_URL, HEADERS, DATA_MAP_URL, DATA_MAP_PATH, METHOD
from generate.fetch_data import fetch_data
from generate.fetch_data_map import fetch_data_map
from survey_model.questions import Questions
from generate import fetch_data, fetch_data_map, generate_columns, generate_questions, generate_data_objects, generate_questions_validator
from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions
from validators import *
from logs import geterrors

def quickcheck_validator():
  print("Test")
  pass

if __name__ == "__main__":
    quickcheck_validator()
    geterrors()