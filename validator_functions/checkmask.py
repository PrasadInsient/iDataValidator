from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from logs import Error, ErrorLog

import pandas as pd

def checkmask(df, source_cols, target_cols, condition):
    """
    Check if target columns contain blank values if source column values meet a specific condition.

    Parameters:
    df (pd.DataFrame): The DataFrame to check.
    source_cols (list): List of source columns to check conditions on.
    target_cols (list): List of target columns to check for blank values.
    condition (str): Condition to check on source columns ('=', 'in', '>').

    Returns:
    pd.Series: Boolean series indicating if the target columns are blank when source columns meet the condition.
    """
    if condition.startswith('='):
        condition_value = int(condition[1:])
        condition_check = df[source_cols] == condition_value
    elif condition.startswith('in'):
        condition_values = list(map(int, condition[2:].strip()[1:-1].split(',')))
        condition_check = df[source_cols].isin(condition_values)
    elif condition.startswith('>'):
        condition_value = int(condition[1:])
        condition_check = df[source_cols] > condition_value
    else:
        raise ValueError("Invalid condition. Use '=', 'in', or '>' for conditions.")

    def check_row(row):
        if condition_check.loc[row.name].any():  # If any source column meets the condition
            return row[target_cols].isnull().all()  # Check if all target columns are blank (NaN)
        return True  # If condition not met, return True by default

    return df.apply(check_row, axis=1)

# Example usage:
data = {
    'source1': [1, 2, 3, 11],
    'source2': [0, 2, 3, 12],
    'target1': [None, 5, None, None],
    'target2': [None, 6, None, None]
}

df = pd.DataFrame(data)
source_cols = ['source1', 'source2']
target_cols = ['target1', 'target2']

# Check for condition value = 1
print(checkmask(df, source_cols, target_cols, '=1'))

# Check for condition value in [1, 2, 3]
print(checkmask(df, source_cols, target_cols, 'in[1,2,3]'))

# Check for condition value > 10
print(checkmask(df, source_cols, target_cols, '>10'))
