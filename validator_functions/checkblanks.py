import pandas as pd
from logs import adderror

def checkblanks(questionid: str, datacols: list, datarow: pd.Series, ignore_cols: list = [], condition: bool = True):
    """
    Performs a blank check on specified columns in a row of data. If any column that is expected to be blank contains a value, 
    an error is logged. Certain columns can be excluded from this check based on the provided list.

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (list): A list of column names that need to be checked for blank values in the data row.
        datarow (pd.Series): A single row from a pandas DataFrame, represented as a pandas Series, that is being checked for blanks.
        ignore_cols (list, optional): A list of columns that should be excluded from the blank check. These columns will be removed from `datacols` before the check is performed. Defaults to an empty list.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the blank check is performed. If `False`, the function skips the check. Defaults to `True`.

    Returns:
        None: The function logs an error through the `adderror` function if any non-blank values are found in columns where blanks are expected. No value is returned.


    Example Usage:
        # Assuming 'datarow' is a row from a pandas DataFrame:

        # Columns to check for blank values
        datacols = ['col1', 'col2', 'col3']

        # Exclude 'col3' from the blank check
        ignore_cols = ['col3']

        # Perform the blank check
        checkblanks('Q1', datacols, datarow, ignore_cols)

    """
    datarow = datarow.copy()  # Create a copy of the data row to avoid modifying the original

    # Remove excluded columns from the list of columns to check
    for col in ignore_cols:
        if col in datacols:
            datacols.remove(col)

    # Perform the blank check if the condition is true
    if condition:
        for column in datacols:
            # If a non-null value is found where a blank is expected, log an error
            if not pd.isnull(datarow[column]):
                adderror(datarow['record'], questionid, column, 'Blank check failed')
