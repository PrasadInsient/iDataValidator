import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions
from typing import List
import pandas as pd
import numpy as np
import re
from validator_functions.record_validator_functions import *
from validator_functions.question_validator_functions import *
import numpy as np


def validate_row(row):
    pass

def record_validator():
    df = DATA.apply(lambda row : validate_row(row),axis=1) #type:ignore
