import pandas as pd
from logs import adderror

def checkexclusive(questionid: str, datacols: list, datarow: pd.Series, exclusive_cols: list = [], 
                   iszerovalid: bool = True, condition: bool = True, oneway: bool = False):
    """
    Performs an exclusivity check on a set of columns in a row of survey data. It ensures that only one "exclusive" option 
    is selected, and optionally, that no other non-exclusive options are selected alongside it. This function can also 
    check for cases where no selection is made at all if the `oneway` flag is enabled.

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (list): A list of column names to check for selections. These represent the set of columns 
                         where responses can be recorded.
        datarow (pd.Series): A single row of data from a pandas DataFrame, where the exclusivity check is performed.
        exclusive_cols (list, optional): A list of column names that represent "exclusive" options. 
                                         These columns should not be selected along with any other columns.
                                         Defaults to an empty list.
        iszerovalid (bool, optional): Determines whether a value of 0 should be considered a valid selection. 
                                      If `True`, 0 is treated as a valid selection. If `False`, 0 is ignored.
                                      Defaults to `True`.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the exclusivity check is 
                                    performed. If `False`, the function does nothing. Defaults to `True`.
        oneway (bool, optional): If `True`, an additional check is performed to ensure that at least one selection 
                                 (exclusive or non-exclusive) is made. Defaults to `False`.

    Returns:
        None: The function logs errors through the `adderror` function if the exclusivity rules are violated. 
              No value is returned.

    Example Usage:
        # Assuming 'datarow' is a row from a pandas DataFrame:
        # Columns representing possible selections, with 'col1' as exclusive
        datacols = ['col1', 'col2', 'col3', 'col4']
        exclusive_cols = ['col1']

        # Perform the exclusive check with 'col1' as the exclusive column
        checkexclusive('Q1', datacols, datarow, exclusive_cols, iszerovalid=False, condition=True)

    """
    # Make a copy of the row to avoid modifying the original
    datarow = datarow.copy()

    # Ensure exclusive columns are included in the datacols list
    for col in exclusive_cols:
        if col not in datacols:
            datacols.append(col)

    # Proceed only if the condition is met
    if condition:
        no_selections = 0
        no_exclusive_selections = 0

        # Loop through the columns and count selections
        for column in datacols:
            # Count valid selections based on iszerovalid
            if pd.notnull(datarow[column]) and (iszerovalid or (not iszerovalid and datarow[column] != 0)):
                if column in exclusive_cols:
                    no_exclusive_selections += 1
                no_selections += 1

        # Check for multiple exclusive selections
        if no_exclusive_selections > 1:
            adderror(datarow['record'], questionid, no_exclusive_selections, 'Exclusive check failed: More than one exclusive selection.')

        # Check if both exclusive and non-exclusive columns are selected
        if no_exclusive_selections > 0 and no_selections > 0:
            adderror(datarow['record'], questionid, no_selections, 'Exclusive check failed: Exclusive and non-exclusive selections both made.')

        # If oneway is enabled, check if no selections were made
        if not oneway and (no_selections == 0 and no_exclusive_selections==0):
            adderror(datarow['record'], questionid, no_selections, 'Exclusive check failed: No selections made.')
