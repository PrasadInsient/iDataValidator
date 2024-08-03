from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions
from typing import List
import pandas as pd
import numpy as np
import re
from validator_functions import *
import numpy as np


def validate_row(row):
    pass

def record_validator():
    df = DATA.apply(lambda row : validate_row(row),axis=1) #type:ignore
