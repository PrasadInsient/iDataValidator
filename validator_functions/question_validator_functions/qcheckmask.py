from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from typing import List
from logs import Error, ErrorLog,adderror

import pandas as pd

def qcheckmask(question_cols: List[str], maskcond_cols: List[str], condition: str, always_showcols: List[str]):
    """
    Check if specified columns contain values that meet a specific condition and log errors.

    Parameters:
    question_cols (list): List of columns to check.
    maskcond_cols (list): List of columns to check conditions on.
    condition (str): Condition to check on columns ('=', 'in', '>').
    always_showcols (list): List of columns that should always have any value including zero.

    Usage:
    # Check if columns in question_cols meet the condition corresponding to columns in maskcond_cols
    checkmask(['A', 'B'], ['ConditionCol1', 'ConditionCol2'], '=1', ['C', 'D'])

    # Check if columns in question_cols meet the condition corresponding to columns in maskcond_cols
    checkmask(['A', 'B'], ['ConditionCol1', 'ConditionCol2'], 'in[1, 2]', ['C', 'D'])

    # Check if columns in question_cols meet the condition corresponding to columns in maskcond_cols
    checkmask(['A', 'B'], ['ConditionCol1', 'ConditionCol2'], '>0', ['C', 'D'])
    """
    if condition.startswith('='):
        condition_value = int(condition[1:])
        condition_check = DATA[maskcond_cols] == condition_value
    elif condition.startswith('in'):
        condition_values = list(map(int, condition[2:].strip()[1:-1].split(',')))
        condition_check = DATA[maskcond_cols].isin(condition_values)
    elif condition.startswith('>'):
        condition_value = int(condition[1:])
        condition_check = DATA[maskcond_cols] > condition_value
    else:
        raise ValueError("Invalid condition. Use '=', 'in', or '>' for conditions.")

    def check_row(row):
        for q_col, m_col in zip(question_cols, maskcond_cols):
            if not pd.isna(row[q_col]) and not condition_check.loc[row.name, m_col]:
                adderror(row['record'], q_col, row[q_col], f"Value {row[q_col]} does not meet the condition {condition} for column {m_col}")
            if pd.isna(row[q_col]) and condition_check.loc[row.name, m_col]:
                adderror(row['record'], q_col, row[q_col], f"Value {row[q_col]} does not meet the condition {condition} for column {m_col}")
        
        for col in always_showcols:
            if pd.isna(row[col]):
                adderror(row['record'], col, row[col], f"Column {col} should always have a value including zero")
                
        return True

    DATA.apply(check_row, axis=1)