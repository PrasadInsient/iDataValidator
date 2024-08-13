import numpy as np
import re
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror
import pandas as pd
import numpy as np
from typing import List, Union, Callable, Optional, Tuple

def checkvalid_logic(logic_label:str,condition: Callable):
    """
    Check for valid logic across all records -- if any records not statisfied, will be add to error log

    Parameters:
    logic_label (str) : Label to log in error log
    condition (function): A function with valid logic.

    Returns:
    None
    
    Usage:
    checkvalidlogic(label, condition)
    """
    filtered_data = DATA[~DATA.apply(condition, axis=1)]
    for index in filtered_data.index:
        adderror(filtered_data.at[index, 'record'], logic_label, "", f'Logic Check failed')

def checkinvalid_logic(logic_label:str,condition: Callable):
    """
    Check for invalid logic across all records -- if any records statisfied, will be add to error log

    Parameters:
    logic_label (str) : Label to log in error log
    condition (function): A function with valid logic.

    Returns:
    None
    
    Usage:
    checkInvalidLogic(label, condition)
    """    
    filtered_data = DATA[DATA.apply(condition, axis=1)]
    for index in filtered_data.index:
        adderror(filtered_data.at[index, 'record'], logic_label, "", f'Logic Check failed')
