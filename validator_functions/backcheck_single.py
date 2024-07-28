from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
from logs import adderror
import pandas as pd
import numpy as np
import re

import pandas as pd
from typing import List
import pandas as pd
from .checkcondition import check_condition
from typing import List, Optional, Any

def backcheck_single(df: pd.DataFrame, source: str, cols_to_check: List[str], condition: Optional[str] = None):
    """
    Check if the source column value matches the cols_to_check index based on condition.

    Parameters:
    df (pd.DataFrame): The DataFrame to check.
    source (str): The source column name to match against cols_to_check.
    cols_to_check (list): List of column names to check.
    condition (str, optional): Condition to check on the columns (supports '=', 'in', 'range'). Default is None.
    """
    def check_row(row):
        source_value = row[source]
        for col in cols_to_check:
            if not check_condition(row[col], condition, source_value):
                adderror(row['record'], col, row[col], f"Value in {source} does not match the condition {condition} for {col}")
        return True

    
    df.apply(check_row, axis=1) #type:ignore
