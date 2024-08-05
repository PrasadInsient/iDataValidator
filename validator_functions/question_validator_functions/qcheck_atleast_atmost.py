from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
from logs import adderror

import pandas as pd
import numpy as np
from typing import List
from .qcheckcondition import qcheck_condition
from validator_functions import *

def atleast_atmost(cols_to_check, condition=None, at_least=None, at_most=None):
    """
    Check if specified columns meet certain conditions and count the number of columns that do.

    Parameters:
    df (pd.DataFrame): The DataFrame to check.
    cols_to_check (str or list): Column name or list of column names to check.
    condition (str, optional): Condition to check on the columns (supports '=', 'in', 'range'). Default is None.
    at_least (int, optional): Minimum number of columns that must meet the condition. Default is None.
    at_most (int, optional): Maximum number of columns that can meet the condition. Default is None.

    Returns:
    pd.DataFrame: DataFrame containing records of validation failures.
    """
    if isinstance(cols_to_check, str):
        cols_to_check = [cols_to_check]

    def check_row(row):
        count = sum(qcheck_condition(row[col],None,condition) for col in cols_to_check)
        if at_least is not None and count < at_least:
            for col in cols_to_check:
                if qcheck_condition(row[col]):
                    adderror(row['record'], col, row[col], f"At least {at_least} columns must meet the condition")
            return False
        if at_most is not None and count > at_most:
            for col in cols_to_check:
                if qcheck_condition(row[col]):
                    adderror(row['record'], col, row[col], f"At most {at_most} columns can meet the condition")
            return False
        return True

    valid_mask = DATA.apply(check_row, axis=1)
