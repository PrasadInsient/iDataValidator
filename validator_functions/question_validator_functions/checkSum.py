from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
from logs import adderror
import pandas as pd
import numpy as np

def checkSum(question:Question, range_type='static', range_value=None, exclude_cols=[]):
    """
    Check if the sum of specified columns in a DataFrame falls within a given range.

    Parameters:
    question (object): The question object containing datacols attribute (list of columns to sum).
    range_type (str): Type of range ('static', 'column', 'sum_columns').
    range_value (tuple, str, list): Range values depending on range_type.
                                    - 'static': (min, max)
                                    - 'column': column name containing the range
                                    - 'sum_columns': list of columns to sum for the range
    exclude_cols (list): List of columns to exclude from summing.
    
    Returns:None

    Usage:
    # Check with static range
    checksum(question, range_type='static', range_value=(5, 15)))

    # Check with range from another column
    checksum(question, range_type='column', range_value='RangeColumn')

    # Check with range as the sum of other columns
    checksum(question, range_type='sum_columns', range_value=['A', 'C'])

    # Check with excluding some columns
    checksum(question, range_type='static', range_value=(5, 15), exclude_cols=['C'])

    """
    if range_type not in ['static', 'column', 'sum_columns']:
        raise ValueError("Invalid range_type. Expected 'static', 'column', or 'sum_columns' for checksum.")

    # Filter out the columns to exclude
    columns_to_sum = [col for col in question.datacols if col not in exclude_cols]
    
    # Calculate the sum of the specified columns
    column_sum = DATA[columns_to_sum].sum(axis=1)
    if range_type == 'static':
        if not isinstance(range_value, tuple) or len(range_value) != 2:
            raise ValueError(f"For 'static' range_type, range_value must be a tuple (min, max) for checksum - {question.id}.")
        min_range, max_range = range_value
        min_range = [min_range] * len(column_sum)
        max_range = [max_range] * len(column_sum)

    elif range_type == 'column':
        if not isinstance(range_value, str) or range_value not in DATA.columns:
            raise ValueError(f"For 'column' range_type, range_value must be a valid column name for checksum - {question.id}.")
        min_range, max_range = DATA[range_value], DATA[range_value]

    elif range_type == 'sum_columns':
        if not isinstance(range_value, list) or not all(col in DATA.columns for col in range_value):
            raise ValueError(f"For 'sum_columns' range_type, range_value must be a list of valid column names for checksum - {question.id}.")
        min_range, max_range = DATA[range_value].sum(axis=1), DATA[range_value].sum(axis=1)

    # Check if the column sum is within the range and log errors
    for index, (sum_val, min_val, max_val) in enumerate(zip(column_sum, min_range, max_range)):
        if not (min_val <= sum_val <= max_val):
            record =DATA.at[index, 'record']
            adderror(record, question.id, sum_val, f"Sum {sum_val} out of range ({min_val}, {max_val})")