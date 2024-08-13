import numpy as np
import re
import pandas as pd
from typing import List, Union, Callable, Optional, Tuple
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror

# Define a type alias for range tuples
RangeTuple = Tuple[Union[int, float], Union[int, float]]

def qvalidate_exclusivity(datacols, data, exclusive_cols):
    for excl_column in exclusive_cols:
        exclusivity_condition_active = (data[excl_column] != 0) & (~data[excl_column].isna())
        other_columns = [col for col in datacols if col != excl_column and col in data.columns]

        for column in other_columns:
            invalid_rows = data[exclusivity_condition_active & (data[column] != 0) & (~data[column].isna())]
            for index in invalid_rows.index:
                adderror(data.at[index, 'record'], column, data.at[index, column], f'Exclusive check failed for {excl_column}')

def qvalidate_single_multiple(questionid, datacols, data, valid_values, optional_cols, at_least, at_most, allowblanks):
    data = data.copy()
    
    for column in datacols:
        if callable(valid_values):
            data['valid_values'] = data.apply(lambda row: valid_values(row, datacols[0]), axis=1)
        else:
            data['valid_values'] = [valid_values] * len(data)
            
        data['valid_values'] = data['valid_values'].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

        allowcolumnnblank = allowblanks or column in optional_cols
        
        invalid_rows = data[
            ~data.apply(
                lambda row: (
                    (allowcolumnnblank and pd.isnull(row[column])) or
                    (not pd.isnull(row[column]) and row[column] in row['valid_values'])
                ),
                axis=1
            )
        ]

        for index in invalid_rows.index:
            adderror(data.at[index, 'record'], column, data.at[index, column], 'Invalid Value')

    for index, row in data.iterrows():
        num_selected = row[datacols].apply(lambda x: pd.notna(x) and x > 0).sum()
        if num_selected < at_least:
            adderror(row['record'], questionid, "", f"Fewer than {at_least} selections made.")
        if num_selected > at_most:
            adderror(row['record'], questionid, "", f"More than {at_most} selections made.")

def qvalidate_number(datacols, data, range_param, allowblanks, optional_cols):
    data = data.copy()
    
    for column in datacols:
        if callable(range_param):
            data['range_limits'] = data.apply(lambda row: range_param(row), axis=1)
        else:
            data['range_limits'] = [range_param] * len(data)
        
        allowcolumnnblank = allowblanks or column in optional_cols
        
        range_invalid_rows = data[
            ~data.apply(
                lambda row: (
                    (allowcolumnnblank and pd.isnull(row[column])) or
                    (not pd.isnull(row[column]) and (row['range_limits'][0] <= row[column] <= row['range_limits'][1]))
                ),
                axis=1
            )
        ]

        for index in range_invalid_rows.index:
            adderror(data.at[index, 'record'], column, data.at[index, column], 'Invalid Value - Out of range')

def qvalidate_text(datacols, data, txt_min_length, txt_max_length, optional_cols):
    for column in datacols:
        for index, value in data[column].items():
            if pd.isna(value):
                if column in optional_cols:
                    continue
                else:
                    adderror(data.at[index, 'record'], column, data.at[index, column], 'Invalid value - Text field')
                    continue

            cleaned_text = re.sub(r'[\s\W]+', '', str(value))

            if (txt_min_length is not None and len(cleaned_text) < txt_min_length) or \
                (txt_max_length is not None and len(cleaned_text) > txt_max_length):
                adderror(data.at[index, 'record'], column, value, f'Text length check failed - {len(cleaned_text)} chars')

def qvalidate_completeness(questionid, datacols, data, required, at_least, at_most,columns_type):
    if required == 1:
        # Define the condition for non-blank responses
        non_blank_condition = lambda x: pd.notna(x) and x != 0 and x != ''
        if columns_type=='number':
            non_blank_condition = lambda x: pd.notna(x) and x != ''

        # Apply the condition across the specified columns and count non-blank responses
        non_blank_counts = data[datacols].apply(lambda col: col.map(non_blank_condition)).sum(axis=1)

        # Check for rows with fewer than 'at_least' valid responses
        fewer_than_min = non_blank_counts < at_least
        for index in data.index[fewer_than_min]:
            adderror(data.at[index, 'record'], questionid, "", f"At least responses check failed - {at_least} valid responses found.")

        # Check for rows with more than 'at_most' valid responses
        more_than_max = non_blank_counts > at_most
        for index in data.index[more_than_max]:
            adderror(data.at[index, 'record'], questionid, "", f"At most responses check failed - {at_least} valid responses found.")

def validatecolumns(
    question_id: str = "",
    srcdatacols: List[str] = [],
    columns_type: str = 'single',
    valid_values: Union[List, Callable, np.ndarray] = [0, 1],
    exclusive_cols: List[str] = [],
    optional_cols: List[str] = [],
    exclude_cols: List[str] = [],
    range_value: Union[RangeTuple, Callable[[pd.Series], RangeTuple]] = (0, 100),
    allow_blanks: bool = False,
    required: int = 1,
    at_most: int = 999,
    at_least: int = 1,
    txt_min_length: Optional[int] = None,
    txt_max_length: Optional[int] = None,
    custom_row_validation: Optional[Callable] = None,
    condition: Optional[Callable] = None,
    skip_check_blank: bool = False
):

    """
    Validate data based on question type, value range, exclusivity, completeness, text length requirements, and custom validation.
    
    Parameters:
        question_id (str): The question id to be tagged in error log/
        srcdatacols (list[str]): column names to check as list of strings
        columns_type (str): The expected column type (default: 'single').
        valid_values (list, np.ndarray or Callable): List, array, or function returning valid values for 'single' and 'multiple' question types.
        exclusive (list): List of column names that are exclusive.
        optional_cols (list): List of columns where blanks are allowed as valid entries.
        exclude_cols (list): List of column names to exclude from validation.
        range_param (RangeTuple or Callable): A tuple specifying lower and upper range or a function returning such a tuple.
        allow_blanks (bool): Whether to allow blank values as valid.
        required (int): If set to 1, at least one of the columns must have a non-zero/non-null entry.
        at_most (int): Maximum number of selections allowed.
        at_least (int): Minimum number of selections required.
        txt_min_length (int): Minimum length of text after removing spaces and special characters, if applicable.
        txt_max_length (int): Maximum length of text after removing spaces and special characters, if applicable.
        custom_row_validation (function): A custom validation function that takes a row as an argument.
        condition (function): A function that takes a row and returns True if the validation should be applied.
        skip_check_blank (bool):  Whether to skip checking for blanks in rows that do not meet the condition
    """
    if condition is None:
        condition = lambda x: True

    # Create a filtered DataFrame based on the condition
    filtered_data = DATA[DATA.apply(condition, axis=1)]
    
    datacols = [col for col in srcdatacols if col not in exclude_cols]

    for col in exclusive_cols:
        if col not in datacols: datacols.append(col)

    # Check for invalid data in rows that do not meet the condition
    if not skip_check_blank:
        for index, row in DATA[~DATA.apply(condition, axis=1)].iterrows():
            for column in datacols:
                if pd.notna(row[column]):
                    adderror(row['record'], column, row[column], f'Invalid data due to condition failure for {column}')
    
    qvalidate_exclusivity(datacols, filtered_data, exclusive_cols)
    
    if columns_type in ['single', 'multiple']:
        qvalidate_single_multiple(question_id, datacols, filtered_data, valid_values, optional_cols, at_least, at_most, allow_blanks)
    elif columns_type == 'number':
        qvalidate_number(datacols, filtered_data, range_value, allow_blanks, optional_cols)
    elif columns_type == 'text':
        qvalidate_text(datacols, filtered_data, txt_min_length, txt_max_length, optional_cols)

    qvalidate_completeness(question_id, datacols, filtered_data, required, at_least, at_most,columns_type)

    # Apply custom row validation to filtered data
    if custom_row_validation is not None:
        filtered_data.apply(custom_row_validation, axis=1)
