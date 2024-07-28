from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from logs import adderror
import pandas as pd
from typing import List
import pandas as pd
from .checkcondition import check_condition

def atleast_atmost(df, cols_to_check, condition=None, at_least=None, at_most=None):
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
        count = sum(check_condition(row[col],None,condition) for col in cols_to_check)
        if at_least is not None and count < at_least:
            for col in cols_to_check:
                if check_condition(row[col]):
                    adderror(row['record'], col, row[col], f"At least {at_least} columns must meet the condition")
            return False
        if at_most is not None and count > at_most:
            for col in cols_to_check:
                if check_condition(row[col]):
                    adderror(row['record'], col, row[col], f"At most {at_most} columns can meet the condition")
            return False
        return True

    valid_mask = df.apply(check_row, axis=1)
    invalid_records = df[~valid_mask]
    return invalid_records

# Example usage:
data = {
    'record': [1, 2, 3, 4],
    'A': [1, None, 3, None],
    'B': [None, 2, 3, None],
    'C': [7, 8, None, None],
    'D': [10, 11, 12, 13]
}

df = pd.DataFrame(data)

# Check for at least 1 non-blank value in specified columns
print(atleast_atmost(df, ['A', 'B', 'C'], at_least=1))

# Check for at most 2 non-blank values in specified columns
print(atleast_atmost(df, ['A', 'B', 'C'], at_most=2))

# Check for condition value = 3
print(atleast_atmost(df, ['A', 'B', 'C', 'D'], condition='=3'))

# Check for condition value in [1, 2, 3]
print(atleast_atmost(df, ['A', 'B', 'C', 'D'], condition='in[1,2,3]'))

# Check for condition value in range [1, 10]
print(atleast_atmost(df, ['A', 'B', 'C', 'D'], condition='range[1,10]'))
