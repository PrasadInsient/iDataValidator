import numpy as np
import re
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror
import pandas as pd
import numpy as np
from typing import List, Union, Callable, Optional, Tuple
# Define a type alias for range tuples
RangeTuple = Tuple[Union[int, float], Union[int, float]]

def qvalidate_exclusivity(question, data, exclusive):
    for excl_column in exclusive:
        if excl_column in data.columns:
            exclusivity_condition_active = (data[excl_column] != 0) & (~data[excl_column].isna())
            other_columns = [col for col in question.datacols if col != excl_column and col in data.columns]

            for column in other_columns:
                invalid_rows = data[exclusivity_condition_active & (data[column] != 0) & (~data[column].isna())]
                for index in invalid_rows.index:
                    adderror(data.at[index, 'record'], column, data.at[index, column], f'Exclusivity violated by {excl_column} being active')

def qvalidate_single_multiple(question, data, valid_values, optional_cols, at_least, at_most):
    for column in question.datacols:
        if column in data.columns:
            if callable(valid_values):
                data['valid_values'] = data.apply(lambda row: valid_values(row), axis=1)
            else:
                data['valid_values'] = [valid_values] * len(data)

            data['valid_values'] = data['valid_values'].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

            if column in optional_cols:
                data['valid_values'] = data['valid_values'].apply(lambda x: x + [pd.NA])

            invalid_rows = data[~data.apply(lambda row: row[column] in row['valid_values'], axis=1)]
            for index in invalid_rows.index:
                adderror(data.at[index, 'record'], column, data.at[index, column], 'Invalid Value')

    for index, row in data.iterrows():
        num_selected = row[question.datacols].apply(lambda x: pd.notna(x) and x > 0).sum()
        if num_selected < at_least:
            adderror(row['record'], question.id, "", f"Fewer than {at_least} selections made.")
        if num_selected > at_most:
            adderror(row['record'], question.id, "", f"More than {at_most} selections made.")

def qvalidate_number(question, data, range_param, allow_blanks, optional_cols):
    for column in question.datacols:
        if column in data.columns:
            if callable(range_param):
                data['range_limits'] = data.apply(lambda row: range_param(row), axis=1)
            else:
                data['range_limits'] = [range_param] * len(data)

            range_invalid_rows = data[~data.apply(lambda row: row['range_limits'][0] <= row[column] <= row['range_limits'][1], axis=1)]

            check_blanks = not allow_blanks and column not in optional_cols
            blank_invalid_rows = data[data[column].isna()] if check_blanks else pd.DataFrame()

            for df in [range_invalid_rows, blank_invalid_rows]:
                for index in df.index:
                    if df is range_invalid_rows:
                        error_value = data.at[index, column]
                        error_message = 'Out of range'
                    else:
                        error_value = 'Blank value not allowed'
                        error_message = 'Blank not allowed'
                    
                    adderror(data.at[index, 'record'], column, error_value, error_message)

def qvalidate_text(question, data, txt_min_length, txt_max_length, optional_cols):
    for column in question.datacols:
        if column in data.columns and (txt_min_length is not None or txt_max_length is not None):
            for index, value in data[column].iteritems():
                if pd.isna(value):
                    if column in optional_cols:
                        continue
                    else:
                        adderror(data.at[index, 'record'], column, 'Blank value', 'Blank not allowed')
                        continue

                cleaned_text = re.sub(r'[\s\W]+', '', str(value))

                if (txt_min_length is not None and len(cleaned_text) < txt_min_length) or \
                   (txt_max_length is not None and len(cleaned_text) > txt_max_length):
                    adderror(data.at[index, 'record'], column, value, f'Text length violation (cleaned length {len(cleaned_text)})')

def qvalidate_completeness(question, data, required, at_least, at_most):
    if required == 1:
        for index, row in data.iterrows():
            non_blank_responses = row[question.datacols].apply(lambda x: pd.notna(x) and x != 0 and x != '').sum()
            
            if non_blank_responses < at_least:
                adderror(data.at[index, 'record'], question.id, "", f"Fewer than {at_least} valid responses found.")
            if non_blank_responses > at_most:
                adderror(data.at[index, 'record'], question.id, "", f"More than {at_most} valid responses found.")

def qcheck_valid(
    question: Question,
    qtype: str = 'single',
    valid_values: Union[List, Callable, np.ndarray] = [0, 1],
    exclusive: List[str] = [],
    optional_cols: List[str] = [],
    exclude_cols: List[str] = [],
    range_value: Union[RangeTuple, Callable[[pd.Series], RangeTuple]] = (0, 100),
    allow_blanks: bool = False,
    required: int = 1,
    at_most: int = 1,
    at_least: int = 1,
    txt_min_length: Optional[int] = None,
    txt_max_length: Optional[int] = None,
    custom_row_validation: Optional[Callable] = None,
    condition: Optional[Callable] = None,
    skip_check_blank=True
):
    """
    Validate data based on question type, value range, exclusivity, completeness, text length requirements, and custom validation.

    Parameters:
        question (Question): The question object with properties like type, datacols, etc.
        qtype (str): The expected question type (default: 'single').
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

    Returns: None

    Usage examples:
    
    # Define a custom row validation function
    def qcustom_row_validation_function(row):
        # Custom validation logic
        for column in row.index:
            if column != 'record' and row[column] % 2 != 0:
                adderror(row['record'], column, row[column], 'Custom validation: Value is not even')

    # Use a lambda function as a condition
    condition = lambda row: row['S1'] in range(1, 5)

    # Example question object
    question = Question(id='Q1', type='number', datacols=['col1', 'col2'])

    # Call check_valid with custom row validation function and condition
    check_valid(question, qtype='number', range_param=(0, 100), custom_row_validation=custom_row_validation_function, condition=condition)
    """
    if question.type != qtype:
        adderror("#NA", question.id, "0", f'{question.id} - question type {question.type} mismatch.')
        return 

    if condition is None:
        condition = lambda x: True

    # Create a filtered DataFrame based on the condition
    filtered_data = DATA[DATA.apply(condition, axis=1)]
    
    # Check for invalid data in rows that do not meet the condition
    if skip_check_blank:
        for index, row in DATA[~DATA.apply(condition, axis=1)].iterrows():
            for column in question.datacols:
                if pd.notna(row[column]):
                    adderror(row['record'], column, row[column], f'Invalid data due to condition failure for {column}')

    qvalidate_exclusivity(question, filtered_data, exclusive)
    
    if question.type in ['single', 'multiple']:
        qvalidate_single_multiple(question, filtered_data, valid_values, optional_cols, at_least, at_most)
    elif question.type == 'number':
        qvalidate_number(question, filtered_data, range_value, allow_blanks, optional_cols)
    elif question.type == 'text':
        qvalidate_text(question, filtered_data, txt_min_length, txt_max_length, optional_cols)

    qvalidate_completeness(question, filtered_data, required, at_least, at_most)

    # Apply custom row validation to filtered data
    if custom_row_validation is not None:
        filtered_data.apply(custom_row_validation, axis=1)

'''   
# Example usage of check_valid function
def qexample_usage():
    # Single choice validation
    check_valid(
        questions['Q1'],
        qtype=QUESTIONTYPES.SINGLE,
        valid_values=np.arange(1, 5),  # Valid values are 1 to 4
        condition=lambda row: True  # Apply to all rows
    )

    # Multiple choice validation
    qcheck_valid(
        questions['Q2'],
        qtype=QUESTIONTYPES.MULTIPLE,
        valid_values=[0, 1],  # Valid values for each choice
        at_least=1,  # At least 1 choice should be selected
        at_most=2,   # At most 2 choices can be selected
        condition=lambda row: True  # Apply to all rows
    )

    # Numeric validation with static range
    qcheck_valid(
        questions['Q3'],
        qtype=QUESTIONTYPES.NUMBER,
        range_param=(10, 100),  # Static range from 10 to 100
        allow_blanks=False,  # Do not allow blanks
        condition=lambda row: True  # Apply to all rows
    )

    # Numeric validation with dynamic range
    qcheck_valid(
        questions['Q3'],
        qtype=QUESTIONTYPES.NUMBER,
        range_param=lambda row: (0, float(row['Q1']) * 10),  # Dynamic range based on Q1
        allow_blanks=False,
        condition=lambda row: True
    )

    # Text validation
    qcheck_valid(
        questions['Q4'],
        qtype=QUESTIONTYPES.TEXT,
        txt_min_length=5,  # Minimum text length
        txt_max_length=15, # Maximum text length
        condition=lambda row: True  # Apply to all rows
    )
'''