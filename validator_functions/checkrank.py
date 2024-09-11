import pandas as pd
from logs import adderror
from typing import List, Optional, Any

def checkrank(questionid: str, datacols: list, datarow: pd.Series, min_rank_value: int = 1, 
              max_rank_value: Optional[int] = None, ignore_cols: list = [], condition: bool = True):
    """
    Perform a rank check on specified columns in a row of survey data. This function ensures that the ranks in 
    `datacols` are unique and within a specified range (from `min_rank_value` to `max_rank_value`).

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (list): A list of column names to check for rank values.
        datarow (pd.Series): A single row from a pandas DataFrame, where the rank check is performed.
        min_rank_value (int, optional): The minimum allowed rank value. Defaults to 1.
        max_rank_value (int, optional): The maximum allowed rank value. If not provided, it defaults to the number 
                                        of columns being checked.
        ignore_cols (list, optional): A list of column names to exclude from the rank check. These columns 
                                       are removed from `datacols` before the check is performed. Defaults to an empty list.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the rank check is performed. 
                                    If `False`, the function does nothing. Defaults to `True`.

    Example Usage:
        # Assuming 'datarow' is a row from a pandas DataFrame:

        # Columns to check for rank values
        datacols = ['col1', 'col2', 'col3', 'col4']

        # Perform the rank check
        checkrank('Q1', datacols, datarow, min_rank_value=1, max_rank_value=4)
    """
    if condition:
        # Filter columns to check based on ignore_cols
        columns_to_check = [col for col in datacols if col not in ignore_cols]
        
        # If max_rank_value is not provided, set it to the number of columns being checked
        if max_rank_value is None:
            max_rank_value = len(columns_to_check)

        # Drop NA values and ensure all values are unique
        values = datarow[columns_to_check].dropna().unique()

        # Check for duplicate rank values
        if len(values) != datarow[columns_to_check].dropna().size:
            adderror(datarow['record'], questionid, "", "checkrank - Duplicate values found.")

        # Check if all rank values are within the allowed range
        elif not all(min_rank_value <= val <= max_rank_value for val in values):
            adderror(datarow['record'], questionid, "", "checkrank - Rank out of range.")
