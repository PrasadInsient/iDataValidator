from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
from logs import adderror
import pandas as pd
import numpy as np
import re

import pandas as pd
from typing import List
import pandas as pd
from typing import List, Optional, Any

from typing import List, Optional
import pandas as pd

def check_condition(value, condition):
    """
    Check if the value satisfies the condition with respect to the source value.

    Parameters:
    value: The value from the column to check.
    condition (str): The condition to check ('=', 'in', 'range', '>').

    Returns:
    bool: True if the condition is satisfied, False otherwise.
    """
    if condition == '=':
        return value == int(condition[1:])
    elif condition == 'in':
        values = list(map(int, condition[2:].strip()[1:-1].split(',')))
        return value in values
    elif condition == 'range':
        try:
            min_val, max_val = map(int, condition[5:].strip()[1:-1].split(','))
            return min_val <= value <= max_val
        except ValueError:
            return False
    elif condition == '>':
        return value > int(condition[1:])
    elif condition == '<':
        return value < int(condition[1:])
    elif condition == '>=':
        return value >= int(condition[2:])
    elif condition == '<=':
        return value <= int(condition[2:])
    return False

def backcheckSingle( question: Question, cols_to_check: List[str], condition: Optional[str] = None):
    """
    Check if the value in cols_to_check[source-1] satisfies the condition based on the source column value.

    Parameters:
    question (question): The index of the source column to match against cols_to_check.
    cols_to_check (list): List of column names to check.
    condition (str, optional): Condition to check on the columns (supports '=', 'in', 'range', '>'). Default is None.
    """
    def check_row(row):
        question_val = row[question.id]
        target_value = row[cols_to_check[question_val - 1]]  # Get value from cols_to_check[source-1]
        if not check_condition(target_value, condition):
            adderror(row['record'], question.id, target_value, f"Backcheck single failed with condition {condition}")
        return True

    DATA.apply(check_row, axis=1)  # Apply the check_row function to each row

# Example usage
# backcheck_single(DATA, 1, ['col1', 'col2'], condition='>')

