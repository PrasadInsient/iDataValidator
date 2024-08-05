from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
from logs import adderror
import pandas as pd
import numpy as np
from .qchecksum import qchecksum

def qchecksum100(question:Question, exclude_cols=[]):
    qchecksum(question, range_type='static', range_value=(1,100), exclude_cols=[])