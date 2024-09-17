import pandas as pd
from typing import List, Union, Callable, Optional, Tuple
from logs import adderror
from .checksum import checksum

from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank  

RangeTuple = Tuple[Union[int, float], Union[int, float]]

def checksum100(questionid, datacols, datarow:pd.Series, sum_condition: str = '=100',ignore_cols=[],condition=True):
    """
    Perform a sum check on specified columns in a row of survey data to 100.

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (list): A list of column names whose values will be summed.
        datarow (pd.Series): A single row from a pandas DataFrame, where the sum check is performed.
        ignore_cols (list, optional): A list of column names to exclude from the sum calculation. These columns 
                                       are removed from `datacols` before the check is performed. Defaults to an empty list.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the sum check is performed. 
                                    If `False`, the function does nothing. Defaults to `True`.


    Example Usage:
        # 
        
        # Columns to check for sum
        datacols = ['col1', 'col2', 'col3', 'col4']

        # Perform the sum check to ensure the sum equals 100
        checksum('Q1', datacols, datarow)

    """    
    checksum(questionid,datacols, datarow, sum_condition,ignore_cols,condition)
    

