from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from logs import Error, ErrorLog
import pandas as pd

from typing import List, Optional, Any

def qcheck_condition(value: Any, source_value: Optional[Any] = None, condition: Optional[str]="=1") -> bool:
    """
    Check if a value meets the specified condition.

    Parameters:
    value (any): The value to check.
    condition (str): The condition to check against (supports '=', 'in', 'range').
    source_value (any, optional): The source value to compare against if needed. Default is None.

    Returns:
    bool: True if the condition is met, False otherwise.
    """
    if condition is None:
        return value == source_value
    elif condition.startswith('='):
        try:
            return value == int(condition[1:])
        except ValueError:
            return False
    elif condition.startswith('in'):
        try:
            values = list(map(int, condition[2:].strip()[1:-1].split(',')))
            return value in values
        except ValueError:
            return False
    elif condition.startswith('range'):
        try:
            min_val, max_val = map(int, condition[5:].strip()[1:-1].split(','))
            if source_value is None:
                return False
            return min_val <= source_value <= max_val
        except ValueError:
            return False
    else:
        raise ValueError("Invalid condition. Supported conditions are '=', 'in', 'range'.")

