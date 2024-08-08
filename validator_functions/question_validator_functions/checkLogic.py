import numpy as np
import re
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror
import pandas as pd
import numpy as np
from typing import List, Union, Callable, Optional, Tuple

def checkValidLogic(logic_label:str,condition: Callable):
    filtered_data = DATA[~DATA.apply(condition, axis=1)]
    for index in filtered_data.index:
        adderror(filtered_data.at[index, 'record'], logic_label, "", f'Logic Check failed')

def checkInvalidLogic(logic_label:str,condition: Callable):
    filtered_data = DATA[DATA.apply(condition, axis=1)]
    for index in filtered_data.index:
        adderror(filtered_data.at[index, 'record'], logic_label, "", f'Logic Check failed')
