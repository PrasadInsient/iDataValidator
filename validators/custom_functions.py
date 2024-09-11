from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Columns, Question, Questions
from typing import List
import pandas as pd
import numpy as np
import re
from validator_functions import *
import numpy as np
from logs import Error, adderror, ErrorLog


'''
added comment 

def S7_validator(row:pd.Series):
    s6 = row['S6']
    s7_sum = row[QUESTIONS.S7.datacols].sum()
    if s7_sum!=s6:
        adderror(row['record'],'S7',s7_sum,"S7 sum check faild")
    if (row['S1']==1 and s7_sum<10) or (row['S1']==2 and s7_sum<5):
        adderror(row['record'],'S7',s7_sum,"S7 term failed")
'''
