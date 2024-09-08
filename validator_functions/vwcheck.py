import pandas as pd
from logs import adderror
from typing import List

def vwcheck(questionid: str, datarow: pd.Series, VW_cols: List[str], condition: bool = True):
    """
    Validates the VW (Value for Money) check based on the specified columns. The check ensures that the values 
    in the specified columns are in increasing order, with each successive value being greater than the previous.

    Parameters:
        questionid (str): The ID of the question being validated (used for logging purposes).
        datarow (pd.Series): A single row from a pandas DataFrame, where the VW check is performed.
        VW_cols (list): A list of column names representing the order of "Too cheap" to "Too expensive".
                        The function checks that these values are in increasing order.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the VW check is performed. 
                                    Defaults to `True`.

    Example Usage:
        # Example datarow from a DataFrame
        datarow = pd.Series({
            'record': '001',
            'too_cheap': 50,
            'affordable': 100,
            'expensive': 150,
            'too_expensive': 200
        })

        # Columns to validate for VW check
        VW_cols = ['too_cheap', 'affordable', 'expensive', 'too_expensive']

        # Perform the VW check
        vwcheck('Q1', datarow, VW_cols)

    """
    if condition:
        # Ensure that at least 3 columns are provided
        if len(VW_cols) >= 3:
            # Check if the first value is less than the second
            if datarow[VW_cols[0]] >= datarow[VW_cols[1]]:
                adderror(datarow['record'], questionid, datarow[VW_cols[0]], "VW check failed")

            # Check if the second value is less than the third
            if datarow[VW_cols[1]] >= datarow[VW_cols[2]]:
                adderror(datarow['record'], questionid, datarow[VW_cols[1]], "VW check failed")

        # If more than 3 columns are provided, perform an additional check
        if len(VW_cols) > 3:
            # Check if the third value is less than the fourth
            if datarow[VW_cols[2]] >= datarow[VW_cols[3]]:
                adderror(datarow['record'], questionid, datarow[VW_cols[2]], "VW check failed")
