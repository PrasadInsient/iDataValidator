from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from logs import Error, ErrorLog, adderror

import pandas as pd

def qcheckrank(question:Question, max_rank_type='static', max_rank_value=None, exclude_cols=[]):
    """
    Check for unique values across specified columns in a DataFrame, ensuring each value is present only once
    and falls within the specified dynamic rank range (min_rank = 1).

    Parameters:
    df (pd.DataFrame): The DataFrame to check.
    question (object): The question object containing datacols attribute (list of columns to check).
    max_rank_type (str): Type of max rank ('static', 'sum_columns', 'column').
    max_rank_value (int, list, str): Max rank value depending on max_rank_type.
                                     - 'static': integer
                                     - 'sum_columns': list of columns to sum for max rank
                                     - 'column': column name containing the max rank
    exclude_cols (list): List of columns to exclude from checking.

    Usage:
    # Check with static max_rank
    print(checkrank(question, max_rank_type='static', max_rank_value=15))

    # Check with max_rank from another column
    print(checkrank(question, max_rank_type='column', max_rank_value='MaxRank'))

    # Check with max_rank as the sum of other columns
    print(checkrank(question, max_rank_type='sum_columns', max_rank_value=['A', 'B']))

    # Check with excluding some columns
    print(checkrank(question, max_rank_type='static', max_rank_value=15, exclude_cols=['D']))
    """
    min_rank = 1

    columns_to_check = [col for col in question.datacols if col not in exclude_cols]

    if max_rank_type == 'static':
        if not isinstance(max_rank_value, int):
            raise ValueError("For 'static' max_rank_type, max_rank_value must be an integer.")
        max_rank = pd.Series([max_rank_value] * len(DATA), index=DATA.index)
    elif max_rank_type == 'sum_columns':
        if not isinstance(max_rank_value, list) or not all(col in DATA.columns for col in max_rank_value):
            raise ValueError("For 'sum_columns' max_rank_type, max_rank_value must be a list of valid column names.")
        max_rank = DATA[max_rank_value].sum(axis=1)
    elif max_rank_type == 'column':
        if not isinstance(max_rank_value, str) or max_rank_value not in DATA.columns:
            raise ValueError("For 'column' max_rank_type, max_rank_value must be a valid column name.")
        max_rank = DATA[max_rank_value]
    else:
        raise ValueError("Invalid max_rank_type. Expected 'static', 'sum_columns', or 'column'.")

    def check_row(row, max_rank_val):
        values = row[columns_to_check].dropna().unique()
        if len(values) != row[columns_to_check].dropna().size:
            for col in columns_to_check:
                if not pd.isna(row[col]):
                    adderror(row['record'], col, row[col], "Duplicate values found.")
            return False
        
        try:
            int_values = list(map(int, values))
        except ValueError:
            for col in columns_to_check:
                if not pd.isna(row[col]):
                    adderror(row['record'], col, row[col], "Non-integer value found.")
            return False

        if not all(min_rank <= val <= max_rank_val for val in int_values):
            for col in columns_to_check:
                if not pd.isna(row[col]) and (int(row[col]) < min_rank or int(row[col]) > max_rank_val):
                    adderror(row['record'], col, row[col], f"Value out of range {min_rank} to {max_rank_val}.")
            return False
        
        return True

    DATA.apply(lambda row: check_row(row, max_rank.loc[row.name]), axis=1)