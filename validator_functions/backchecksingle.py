from logs import adderror
import pandas as pd
from typing import List, Optional, Any
from .checkcondition import checkcondition

def backchecksingle(questionid: str, datarow: pd.Series,qcol: str,  cols_to_check: List[str], 
                     backcheckcondition: str, condition: bool = True):
    """
    Perform a backcheck on a single question in a survey data row. This function verifies the value of a specified column
    (`qcol`) and checks whether the corresponding value in `cols_to_check` satisfies a given condition.

    Parameters:
        questionid (str): The ID of the question being checked.
        qcol (str): The column name from `datarow` to be validated (represents a question in the survey).
        datarow (pd.Series): The row of survey data being processed. Each row is treated as a pandas Series.
        cols_to_check (List[str]): A list of column names to backcheck against. The column to check is determined by the 
                                   value of `question_val` in the `qcol` column.
        maskcondition (Optional[str]): A condition string that the target value must satisfy (e.g., '>', '<', '==').
                                       If not provided, no condition check will be applied.
        condition (bool): A flag to enable or disable the check. If `True`, the function will run; otherwise, it will skip.

    Raises:
        None: Errors are logged through the `adderror` function, rather than raised directly.
    
    Example Usage:
        # Assuming 'datarow' is a row from a pandas DataFrame:
        # Columns in 'cols_to_check' are ['col1', 'col2'] and the question column is 'qcol'.
        # Check if the value in the corresponding column (cols_to_check[source - 1]) satisfies the condition '> 10'.
        
        backchecksingle('Q1', 'qcol', datarow, ['col1', 'col2'], maskcondition='> 10')

    """
    
    if condition:       
        question_val = datarow[qcol]  # Extract the value from qcol (usually a numeric value representing a choice)
        
        if question_val - 1 < len(cols_to_check):
            target_value = datarow[cols_to_check[question_val - 1]]  # Get value from cols_to_check[source-1]
        
            # Check if the target_value satisfies the maskcondition
            if not checkcondition(target_value, backcheckcondition):
                # Log an error if the condition is not satisfied
                adderror(datarow['record'], questionid, target_value, f"Backcheck single failed")
        else:
            # Log an error if the question_val is out of bounds for cols_to_check
            adderror(datarow['record'], questionid, question_val, f"Backcheck single failed")
