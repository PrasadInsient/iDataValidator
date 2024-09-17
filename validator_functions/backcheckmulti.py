import pandas as pd
from typing import  List, Optional, Union
from logs import Error, ErrorLog,adderror
from validator_functions.checkcondition import checkcondition
import pandas as pd



class Question:
    def __init__(self,id, type, parent_record,datacols=[],oecols=[]):
        self.id:str = id
        self.type:str = type
        self.datacols:List[str] = datacols
        self.oecols:List[str] = oecols
        self.parent_record = parent_record

def backcheckmulti(questionid: str, datarow: pd.Series,question_cols: Union[List[str],Question],  cols_to_check: Union[List[str],Question],backcheckcondition: str ="=1",  
        always_showcols: Union[List[str],Question]=[],ignoresourcecols:List[str]=[],ignoretargetcols:List[str]=[],condition= True):

    """

        Back checks slections on specified columns in a row of survey data. The function checks whether certain 
    columns (from `question_cols`) is selcted are satisfying corresponding columns 
    in `maskcond_cols`. If any condition is violated, an error is logged.

    Parameters:
        questionid (str): The ID of the question being checked (used for logging purposes).
        datarow (pd.Series): A single row from a pandas DataFrame, where the masking check is performed.
        question_cols (List[str]): A list of column names representing questions to be checked for masking.
        maskcond_cols (List[str]): A list of corresponding column names that contain the conditions to check for each question.
        maskcondition (str, optional): The condition to check on `maskcond_cols` (e.g., '=1', 'in[1, 2]', '>0'). 
                                       Defaults to '=1'.
        always_showcols (List[str], optional): A list of column names that should always be shown, regardless of 
                                               the masking condition. These columns are excluded from the regular masking check.
                                               Defaults to an empty list.
        condition (bool, optional): A flag to enable or disable the check. If `True`, the masking check is performed. 
                                    If `False`, the function does nothing. Defaults to `True`.

    Returns:
        None: The function logs errors through the `adderror` function if the masking rules are violated. 
              No value is returned.
    
    Example Usage:
        # Assuming 'datarow' is a row from a pandas DataFrame:

        # Columns to check for masking
        question_cols = ['A', 'B']
        maskcond_cols = ['ConditionCol1', 'ConditionCol2']

        # Columns that should always be shown
        always_showcols = ['C', 'D']

        # Perform the masking check
        checkmasking('Q1', datarow, question_cols, maskcond_cols, '=1', always_showcols)

    """
    if condition:
        # Create a copy of the row to avoid modifying the original data
        datarow = datarow.copy()

        if isinstance(question_cols, Question):
            question_cols = question_cols.datacols
        if isinstance(cols_to_check, Question):
            cols_to_check = cols_to_check.datacols
        if isinstance(always_showcols, str):
            always_showcols=[always_showcols]

        # Exclude columns in always_showcols from question_cols
        question_cols = [col for col in question_cols if col not in always_showcols and col not in ignoretargetcols]

        cols_to_check = [col for col in cols_to_check if col not in ignoresourcecols]
        
        # Perform the regular masking check on question_cols and maskcond_cols
        for q_col, m_col in zip(question_cols, cols_to_check):
            # If a question column contains a value, but the mask condition is not satisfied, log an error
            if not pd.isna(datarow[q_col]) and not checkcondition(datarow[m_col], backcheckcondition):
                adderror(datarow['record'], questionid, datarow[q_col], f"Backcheck multi failed")

        # Check the always_showcols to ensure they always have a value (not null)
        for col in always_showcols:
            if pd.isna(datarow[col]):
                adderror(datarow['record'], questionid, datarow[col], f"Backcheck multi failed")
