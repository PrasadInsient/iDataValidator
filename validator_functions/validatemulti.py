import pandas as pd
from logs import adderror

def validatemulti(questionid: str, datacols: list, datarow: pd.Series, valid_values: list = [0,1], optional_cols: list = [], 
                exclusive_cols: list = [], ignore_cols: list = [], at_least: int = 1, at_most: int = -1, 
                  allowblanks: bool = False, required: int = 1, condition: bool = True):
    """
    Perform a multi-select validation on a set of columns in a row of survey data. This function checks if the selected
    values are valid, enforces exclusive selection rules, and ensures that at least or at most a certain number of options 
    are selected. It also handles optional columns and blanks.

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (list): A list of column names to be checked for valid multi-select values.
        datarow (pd.Series): A single row from a pandas DataFrame, where the multi-select validation is performed.
        valid_values (list, optional): A list of valid values for the multi-select columns. Defaults to [0,1].
        optional_cols (list, optional): Columns where blank values are allowed. Defaults to an empty list.
        ignore_cols (list, optional): Columns to exclude from the multi-select validation. These columns are removed 
                                       from `datacols` before the check is performed. Defaults to an empty list.
        exclusive_cols (list, optional): Columns that should behave exclusively (i.e., only one can be selected).
                                         Defaults to an empty list.
        at_least (int, optional): The minimum number of selections required. Defaults to 1.
        at_most (int, optional): The maximum number of selections allowed. If set to -1, no limit is imposed. Defaults to -1.
        allowblanks (bool, optional): Whether blank values are allowed in the multi-select columns. Defaults to False.
        required (int, optional): A flag to enforce the requirement of at least one selection. Defaults to 1 (True).
        condition (bool, optional): A flag to enable or disable the check. If `True`, the multi-select validation is 
                                    performed. If `False`, only a blank check is performed. Defaults to `True`.

    Example Usage:
        # Example datarow from a DataFrame
        datarow = pd.Series({
            'record': '001',
            'col1': 1,
            'col2': 0,
            'col3': 1,
            'col4': None
        })

        # Columns to validate for multi-select
        datacols = ['col1', 'col2', 'col3', 'col4']

        # Perform the multi-select validation with at least 1 and at most 2 selections
        validatemulti('Q1', datacols, datarow, at_least=1, at_most=2, exclusive_cols=['col1'], optional_cols=['col4'])

    """
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

        # Loop through the columns to validate the selections
        for column in datacols:
            allowcolumnblank = allowblanks or column in optional_cols
            # Check if the value is valid or if blank values are allowed
            if (not allowcolumnblank and pd.isnull(datarow[column])) or (pd.notnull(datarow[column]) and datarow[column] not in valid_values):
                adderror(datarow['record'], column, datarow[column], 'Invalid Value')

            # Count valid selections and exclusive selections
            if pd.notnull(datarow[column]) and datarow[column] == 1:
                if column in exclusive_cols:
                    no_exclusive_selections += 1
                else:
                    no_non_exclusive_selections += 1
                no_selections += 1

        # Check for at least one required selection
        if required and no_selections == 0:
            adderror(datarow['record'], questionid, no_selections, 'Multi at least 1 check failed.')

        # Check for at least N selections if required
        elif required:
            if no_exclusive_selections == 0 and at_least > 1 and no_selections < at_least:
                adderror(datarow['record'], questionid, no_selections, 'Multi at least N check failed.')

            # Check for at most N selections if required
            if no_exclusive_selections == 0 and at_most > 1 and no_selections > at_most:
                adderror(datarow['record'], questionid, no_selections, 'Multi at most N check failed.')

        # Check if both exclusive and non-exclusive selections were made
        if no_non_exclusive_selections > 0 and no_exclusive_selections > 0:
            adderror(datarow['record'], questionid, no_selections, 'Multi exclusive check failed.')

    # If condition is False, perform only a blank check
    else:
        for column in datacols:
            if not pd.isnull(datarow[column]):
                adderror(datarow['record'], column, datarow[column], 'Blank check failed')
