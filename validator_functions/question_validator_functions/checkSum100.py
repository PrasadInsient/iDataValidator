from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
from logs import adderror
import pandas as pd
import numpy as np
from .checksum import checksum

def checksum100(question:Question, exclude_cols=[]):
    """
    Check for the sum of values in the quesiton is eqial to 100

    Parameters:
    question (object): The question object containing datacols attribute (list of columns to sum).
    exclude_cols (list): List of columns to exclude from summing.
    
    Returns:None

    Usage:
    # Check with question
    checksum100(question)

    # Check with excluding some columns
    checksum100(question, exclude_cols=['C'])

    """    
    checksum(question, range_type='static', range_value=(1,100), exclude_cols=[])