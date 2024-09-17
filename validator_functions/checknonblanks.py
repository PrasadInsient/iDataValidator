import pandas as pd
from logs import adderror
from isblank import isblank
from isnotblank import isnotblank


def checknonblanks(questionid: str, datacols: list, datarow: pd.Series, ignore_cols: list = [], condition: bool = True):
    """
    Perform a non-blank check on specified columns in a row of survey data. The function checks if the specified columns 
    in `datacols` are non-null (not blank). If any column is found to be null, an error is logged.

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (list): A list of column names to be checked for non-blank (non-null) values.
        datarow (pd.Series): A single row from a pandas DataFrame, where the non-blank check is performed.
        ignore_cols (list, optional): A list of column names to exclude from the non-blank check. These columns 
                                       are removed from `datacols` before the check is performed. Defaults to an empty list.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the non-blank check is performed. 
                                    If `False`, the function does nothing. Defaults to `True`.

    Example Usage:
        # Assuming 'datarow' is a row from a pandas DataFrame:

        # Columns to check for non-blank values
        datacols = ['col1', 'col2', 'col3']

        # Exclude 'col3' from the non-blank check
        ignore_cols = ['col3']

        # Perform the non-blank check
        checknonblanks('Q1', datacols, datarow, ignore_cols)

    """
    # Create a copy of the row to avoid modifying the original data
    datarow = datarow.copy()

    # Remove excluded columns from the list of columns to check
    for col in ignore_cols:
        if col in datacols:
            datacols.remove(col)

    # Perform the non-blank check if the condition is true
    if condition:
        for column in datacols:
            # If a column is null (blank), log an error
            if isblank(datarow[column]):
                adderror(datarow['record'], column, datarow[column], 'Non blank check failed')
