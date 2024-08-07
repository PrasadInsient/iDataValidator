from typing import Callable, List, Optional, Union
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
from logs import adderror

import pandas as pd
import numpy as np
import re

def checkNonBlanks(cols_to_check:Union[List, Question],condition: Optional[Callable] = None):
    """
    Check if specified columns contain blank (NaN) values.

    Parameters:
    df (pd.DataFrame): The DataFrame to check.
    cols_to_check (str or list): Column name or list of column names to check for blank values.

    Returns:
    pd.Series: Boolean series indicating if the specified columns are blank for each row.
    
    Usage:
    check_for_blanks('A'))
    check_for_blanks(['A','B']))
    """
    if isinstance(cols_to_check, str):
        xcols_to_check = [cols_to_check]

    if isinstance(cols_to_check, Question):
        xcols_to_check = cols_to_check.datacols

    if condition is None:
        condition = lambda x: True

    # Create a filtered DataFrame based on the condition
    filtered_data = DATA[DATA.apply(condition, axis=1)]

    def check_row(row):
        for col in xcols_to_check:
            value = row[col]
            if pd.isna(value):
                adderror(row['record'], col, row[col], f"Non blank check failed")
        return True  # Return True to satisfy the return type expected by apply


    # Apply the check_row function to each row
    filtered_data.apply(check_row, axis=1)
