from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from typing import Callable, List, Optional
from logs import Error, ErrorLog,adderror
import pandas as pd
from .checkmasking import checkmasking

def checkquestion_mask(question: Question, mask_question: Question, maskcondition: str ="=1",  always_showcols: List[str]=[], condition: Optional[Callable] = None):
    """
    Check if question contain values that meet a specific condition and log errors.

    Parameters:
    question (Question): Question object
    mask_question (Question): Question object
    condition (str): Condition to check on columns ('=', 'in', '>').
    always_showcols (list): List of columns that should always have any value including zero.

    Usage:
    # Check if columns in question_cols meet the condition corresponding to columns in maskcond_cols
    checkquestion_mask(question, mask_question, '=1', ['C', 'D'])

    # Check if columns in question_cols meet the condition corresponding to columns in maskcond_cols
    checkquestion_mask(question, mask_question, 'in[1, 2]', ['C', 'D'])

    # Check if columns in question_cols meet the condition corresponding to columns in maskcond_cols
    checkquestion_mask(question, mask_question, '>0', ['C', 'D'])
    """
    checkmasking(question.datacols, mask_question.datacols, maskcondition, always_showcols,condition)