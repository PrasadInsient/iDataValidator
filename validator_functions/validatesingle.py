import pandas as pd
from logs import adderror
from validator_functions import checkblanks
from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank  

def validatesingle(questionid: str, datacols: list, datarow: pd.Series, valid_values: list, 
                   optional_cols: list = [], ignore_cols: list = [], allowblanks: bool = False, condition: bool = True):
    """
    Perform single-value validation on specified columns in a row of survey data. The function checks if the values 
    in `datacols` are valid according to the provided `valid_values` list, optionally allows blanks, and excludes 
    certain columns from validation if needed.

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (list): A list of column names to be checked for valid single values.
        datarow (pd.Series): A single row from a pandas DataFrame, where the single-value validation is performed.
        valid_values (list): A list of valid values that the data in `datacols` should match.
        optional_cols (list, optional): A list of columns where blank values are allowed. Defaults to an empty list.
        ignore_cols (list, optional): A list of columns to exclude from the single-value validation. These columns 
                                       are removed from `datacols` before the check is performed. Defaults to an empty list.
        allowblanks (bool, optional): Whether blank values are allowed in the columns. Defaults to False.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the single-value validation 
                                    is performed. If `False`, the function only performs a blank check. Defaults to `True`.

    Example Usage:
        # Example datarow from a DataFrame
        datarow = pd.Series({
            'record': '001',
            'col1': 5,
            'col2': 3,
            'col3': None
        })

        # Columns to validate
        datacols = ['col1', 'col2', 'col3']

        # Perform single-value validation allowing values from 1 to 5
        validatesingle('Q1', datacols, datarow, valid_values=[1, 2, 3, 4, 5])

    """
    # Make a copy of the data row to avoid modifying the original
    datarow = datarow.copy()

    # Remove any excluded columns from datacols
    for col in ignore_cols:
        if col in datacols:
            datacols.remove(col)

    # Perform the validation check
    if condition:
        for column in datacols:
            allowcolumnblank = allowblanks or column in optional_cols
            # Check if the value is valid or if blanks are allowed
            if (not allowcolumnblank and pd.isnull(datarow[column])) or (pd.notnull(datarow[column]) and datarow[column] not in valid_values):
                adderror(datarow['record'], column, datarow[column], 'Invalid Value')
    else:
        checkblanks(questionid,datacols,datarow)
        # If the condition is False, check only for blanks
#        for column in datacols:
#            if not pd.isnull(datarow[column]):
#                adderror(datarow['record'], questionid, datarow[column], 'Blank check failed')
