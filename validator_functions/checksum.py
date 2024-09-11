import pandas as pd
from logs import adderror

def checksum(questionid: str, datacols: list, datarow: pd.Series, sum_condition: str = '=100', ignore_cols: list = [], condition: bool = True):
    """
    Perform a sum check on specified columns in a row of survey data. The function checks if the sum of the values in 
    `datacols` meets the condition specified in `sum_condition` (e.g., '=100', '<50', '>20', 'range(90,110)').

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datacols (list): A list of column names whose values will be summed.
        datarow (pd.Series): A single row from a pandas DataFrame, where the sum check is performed.
        ignore_cols (list, optional): A list of column names to exclude from the sum calculation. These columns 
                                       are removed from `datacols` before the check is performed. Defaults to an empty list.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the sum check is performed. 
                                    If `False`, the function does nothing. Defaults to `True`.
        sum_condition (str, optional): A string representing the condition to check the sum against. This can be:
                                       - '=X' to check if the sum equals X
                                       - '<X' to check if the sum is less than X
                                       - '>X' to check if the sum is greater than X
                                       - 'range(X,Y)' to check if the sum is within the range X to Y (inclusive)
                                       Defaults to '=100'.

    Example Usage:
        # Example datarow from a DataFrame
        datarow = pd.Series({
            'record': '001',
            'col1': 50,
            'col2': 30,
            'col3': 20,
            'col4': None
        })

        # Columns to check for sum
        datacols = ['col1', 'col2', 'col3', 'col4']

        # Perform the sum check to ensure the sum equals 100
        checksum('Q1', datacols, datarow, sum_condition='=100')

        # Perform the sum check to ensure the sum is within the range 90 to 110
        checksum('Q1', datacols, datarow, sum_condition='range(90,110)')
    """
    # Make a copy of the data row to avoid modifying the original
    datarow = datarow.copy()

    # Remove any excluded columns from datacols
    for col in ignore_cols:
        if col in datacols:
            datacols.remove(col)

    if condition:
        # Calculate the sum of the specified data columns
        sumx = datarow[datacols].sum()
        
        # Define the sum checks based on the sum_condition parameter
        if sum_condition.startswith('='):
            target = float(sum_condition[1:])
            if sumx != target:
                adderror(datarow['record'], questionid, sumx, f'Sum check failed: expected {target}, got {sumx}')
        
        elif sum_condition.startswith('<'):
            target = float(sum_condition[1:])
            if sumx >= target:
                adderror(datarow['record'], questionid, sumx, f'Sum check failed: sum is not < {target}')
        
        elif sum_condition.startswith('>'):
            target = float(sum_condition[1:])
            if sumx <= target:
                adderror(datarow['record'], questionid, sumx, f'Sum check failed: sum is not > {target}')
        
        elif sum_condition.startswith('range'):
            lower_bound, upper_bound = map(float, sum_condition[6:-1].split(','))
            if not (lower_bound <= sumx <= upper_bound):
                adderror(datarow['record'], questionid, sumx, f'Sum check failed: sum is not in range ({lower_bound}, {upper_bound})')
        
        else:
            adderror(datarow['record'], questionid, sumx, 'Invalid sum condition provided')

