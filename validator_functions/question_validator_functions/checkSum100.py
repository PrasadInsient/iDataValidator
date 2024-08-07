from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
from logs import adderror
import pandas as pd
import numpy as np
from .checkSum import checkSum

def checkSum100(question:Question, exclude_cols=[]):
    checkSum(question, range_type='static', range_value=(1,100), exclude_cols=[])