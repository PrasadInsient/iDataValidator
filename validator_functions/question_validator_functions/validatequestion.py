import numpy as np
import re
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror
import pandas as pd
import numpy as np
from typing import List, Union, Callable, Optional, Tuple
from .validatecolumns import *

def validatequestion(
    question: Question,
    qtype: str = 'single',
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
    skip_check_blank=False
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
        skip_check_blank (bool):  Whether to skip checking for blanks in rows that do not meet the condition

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

    # Call  with custom row validation function and condition
    validatequestion(question, qtype='number', range_param=(0, 100), custom_row_validation=custom_row_validation_function, condition=condition)
    """
    srcdatacols = question.datacols

    if question.type != qtype:
        adderror("#NA", question.id, "0", f'{question.id} - question type {question.type} mismatch.')
        return
    validatecolumns(question.id,srcdatacols,question.type,valid_values,
                    exclusive_cols,optional_cols,exclude_cols,
                    range_value,allow_blanks,required,at_most,at_least,txt_min_length,txt_max_length,
                    custom_row_validation,condition,skip_check_blank
                    )
    

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