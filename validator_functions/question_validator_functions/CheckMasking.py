from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from typing import Callable, List, Optional
from logs import Error, ErrorLog,adderror

import pandas as pd

def checkmasking(question_cols: List[str], maskcond_cols: List[str], maskcondition: str ="=1",  always_showcols: List[str]=[], condition: Optional[Callable] = None):
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
    if maskcondition.startswith('='):
        condition_value = int(maskcondition[1:])
        condition_check = DATA[maskcond_cols] == condition_value
    elif maskcondition.startswith('in'):
        condition_values = list(map(int, maskcondition[2:].strip()[1:-1].split(',')))
        condition_check = DATA[maskcond_cols].isin(condition_values)
    elif maskcondition.startswith('>'):
        condition_value = int(maskcondition[1:])
        condition_check = DATA[maskcond_cols] > condition_value
    elif maskcondition.startswith('<'):
        condition_value = int(maskcondition[1:])
        condition_check = DATA[maskcond_cols] < condition_value
    elif maskcondition.startswith('>='):
        condition_value = int(maskcondition[2:])
        condition_check = DATA[maskcond_cols] >= condition_value
    elif maskcondition.startswith('<='):
        condition_value = int(maskcondition[2:])
        condition_check = DATA[maskcond_cols] <= condition_value
    else:
        raise ValueError("checkmasking - Invalid condition. Use '=', 'in', or '>' for conditions.")

    def check_row(row):
        for q_col, m_col in zip(question_cols, maskcond_cols):
            if not pd.isna(row[q_col]) and not condition_check.loc[row.name, m_col]:
                adderror(row['record'], q_col, row[q_col], f"checkmasking - Value {row[q_col]} does not meet the condition {condition} for column {m_col}")
            if pd.isna(row[q_col]) and condition_check.loc[row.name, m_col]:
                adderror(row['record'], q_col, row[q_col], f"checkmasking - Value {row[q_col]} does not meet the condition {condition} for column {m_col}")
        
        for col in always_showcols:
            if pd.isna(row[col]):
                adderror(row['record'], col, row[col], f"checkmasking - Always show Column {col} missing data")
                
        return True
    
    if condition is None:
        condition = lambda x: True

    # Create a filtered DataFrame based on the condition
    filtered_data = DATA[DATA.apply(condition, axis=1)]
    
    filtered_data.apply(check_row, axis=1)