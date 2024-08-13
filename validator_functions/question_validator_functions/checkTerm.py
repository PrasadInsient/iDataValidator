import numpy as np
import re
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror
import pandas as pd
import numpy as np
from typing import List, Union, Callable, Optional, Tuple
# Define a type alias for range tuples
RangeTuple = Tuple[Union[int, float], Union[int, float]]

def checkterm(term_label:str,condition: Callable):
    """
    Check for termination logic -- no records should be in the data satisfying this condition. If there, add to error log. 

    Parameters:
    term_label: A label to add in error log if termination fails
    condition :  A function that takes a row and returns True if the validation should be applied
    Returns:None

    Usage:
    # Check with static range
    checkterm(term_label, condition=custom_row_validation_function )

    """
    filtered_data = DATA[DATA.apply(condition, axis=1)]
    for index in filtered_data.index:
        adderror(filtered_data.at[index, 'record'], term_label, "", f'Term Check failed')
