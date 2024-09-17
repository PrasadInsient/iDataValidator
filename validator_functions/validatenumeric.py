import pandas as pd
from typing import List, Union, Tuple
from logs import adderror
from validator_functions import checkblanks

from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank  

# Define a type alias for the range parameter (min, max)
RangeTuple = Tuple[Union[int, float], Union[int, float]]

def validatenumeric(questionid: str, datacols: List[str], datarow: pd.Series, optional_cols: List[str] = [], 
                    exclusive_cols: List[str] = [], ignore_cols: List[str] = [], at_least: int = 1, 
                    at_most: int = -1, allowblanks: bool = False, required: int = 1, condition: bool = True, 
                    range_param: RangeTuple = (0, 100)):
    """
    Perform numeric validation on specified columns in a row of survey data. The function checks whether the values 
    in `datacols` fall within the range specified by `range_param`, enforces exclusive selection rules, and ensures 
    that at least or at most a certain number of valid values are selected. It also handles optional columns and blanks.

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (List[str]): A list of column names to be checked for valid numeric values.
        datarow (pd.Series): A single row from a pandas DataFrame, where the numeric validation is performed.
        optional_cols (List[str], optional): A list of columns where blank values are allowed. Defaults to an empty list.
        ignore_cols (List[str], optional): A list of columns to exclude from the numeric validation. These columns 
                                            are removed from `datacols` before the check is performed. Defaults to an empty list.
        exclusive_cols (List[str], optional): Columns that should behave exclusively (i.e., only one can be selected).
                                              Defaults to an empty list.
        at_least (int, optional): The minimum number of valid values required. Defaults to 1.
        at_most (int, optional): The maximum number of valid values allowed. If set to -1, no limit is imposed. Defaults to -1.
        allowblanks (bool, optional): Whether blank values are allowed in the numeric columns. Defaults to False.
        required (int, optional): A flag to enforce the requirement of at least one valid value. Defaults to 1 (True).
        condition (bool, optional): A flag to enable or disable the check. If `True`, the numeric validation is 
                                    performed. If `False`, the function performs a blank check. Defaults to `True`.
        range_param (RangeTuple, optional): A tuple specifying the valid range for the numeric values (min, max). 
                                            Defaults to (0, 100).

    Example Usage:
        # Example datarow from a DataFrame
        datarow = pd.Series({
            'record': '001',
            'col1': 75,
            'col2': 105,
            'col3': 50,
            'col4': None
        })

        # Columns to validate for numeric values
        datacols = ['col1', 'col2', 'col3', 'col4']

        # Perform numeric validation with a valid range of 0 to 100
        validatenumeric('Q1', datacols, datarow, range_param=(0, 100))

    """
    # Make a copy of the data row to avoid modifying the original
    datarow = datarow.copy()

    # Ensure exclusive columns are included in the datacols list
    for col in exclusive_cols:
        if col not in datacols:
            datacols.append(col)

    # Remove any excluded columns from datacols
    for col in ignore_cols:
        if col in datacols:
            datacols.remove(col)

    if condition:
        no_selections = 0
        no_exclusive_selections = 0
        no_non_exclusive_selections=0

        # Loop through the columns to validate the numeric values
        for column in datacols:
            # Skip the validation for exclusive columns
            if column not in exclusive_cols:
                allowcolumnblank = allowblanks or column in optional_cols
                # Check if the value is within the valid range or if blanks are allowed
                if (not allowcolumnblank and pd.isnull(datarow[column])) or (pd.notnull(datarow[column]) and not (range_param[0] <= datarow[column] <= range_param[1])):
                    adderror(datarow['record'], column, datarow[column], 'Invalid Value')

            # Count valid selections and exclusive selections
            if pd.notnull(datarow[column]):
                no_selections += 1
                if column in exclusive_cols:
                    no_exclusive_selections += 1
                else:
                    no_non_exclusive_selections += 1

        # Check for at least one required valid value
        if required and no_selections == 0:
            adderror(datarow['record'], questionid, no_selections, 'Numeric at least 1 check failed.')

        # Check for at least N valid values
        elif required:
            if no_exclusive_selections == 0 and at_least > 1 and no_selections < at_least:
                adderror(datarow['record'], questionid, no_selections, 'Numeric at least N check failed.')

            # Check for at most N valid values
            if no_exclusive_selections == 0 and at_most > 1 and no_selections > at_most:
                adderror(datarow['record'], questionid, no_selections, 'Numeric at most N check failed.')

        # Check if both exclusive and non-exclusive selections were made
        if no_non_exclusive_selections > 0 and no_exclusive_selections > 0:
            adderror(datarow['record'], questionid, no_selections, 'Numeric exclusive check failed.')

    # If condition is False, perform only a blank check
    else:
        checkblanks(questionid,datacols,datarow)
#        for column in datacols:
#            if not pd.isnull(datarow[column]):
#                adderror(datarow['record'], questionid, datarow[column], 'Blank check failed')
