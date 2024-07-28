from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror
import pandas as pd
import numpy as np
import re


def check_valid(question:Question, qtype='single', valid_values=[0, 1], exclusive=[], llimit=0, ulimit=100, 
                allow_blanks=False, required=1, txt_min_length=None, txt_max_length=None):
    """
    Validate data based on question type, value range, exclusivity, completeness, and text length requirements.

    Parameters:
        question (Question): The question object with properties like type, datacols, etc.
        DATA (pd.DataFrame): DataFrame containing the data to validate.
        valid_values (list): List of valid values for 'single' and 'multiple' question types.
        exclusive (list): List of column names that are exclusive.
        llimit, ulimit (int): Lower and upper limits for 'number' type validation.
        allow_blanks (bool): Whether to allow blank values as valid.
        required (int): If set to 1, at least one of the columns must have a non-zero/non-null entry.
        txt_min_length (int): Minimum length of text after removing spaces and special characters, if applicable.
        txt_max_length (int): Maximum length of text after removing spaces and special characters, if applicable.

    Returns: None

    Usage:
    
        
    """

    if question.type!=qtype:
        adderror("#NA",question.id,"0",f'{question.id} - question type {question.type} mismatch.')
        return 
    # Validate exclusivity rules
    for excl_column in exclusive:
        if excl_column in DATA.columns:
            exclusivity_condition_active = (DATA[excl_column] != 0) & (~DATA[excl_column].isna())
            other_columns = [col for col in question.datacols if col != excl_column and col in DATA.columns]

            for column in other_columns:
                invalid_rows = DATA[exclusivity_condition_active & (DATA[column] != 0) & (~DATA[column].isna())]
                for index in invalid_rows.index:
                    adderror(DATA.at[index, 'record'],column,DATA.at[index, column],f'Exclusivity violated by {excl_column} being active')

    # Type-specific validation
    for column in question.datacols:
        if column not in DATA.columns:
            continue
        
        if question.type in ['single', 'multiple']:
            invalid_rows = DATA[~DATA[column].isin(valid_values)]
            for index in invalid_rows.index:
                adderror(DATA.at[index, 'record'],column,DATA.at[index, column],f'Invalid Value')

        elif question.type == 'number':
            # Range checks and blank handling
            range_invalid_rows = DATA[(~DATA[column].isna()) & ((DATA[column] < llimit) | (DATA[column] > ulimit))]
            blank_invalid_rows = DATA[DATA[column].isna()] if not allow_blanks else pd.DataFrame()

            for df in [range_invalid_rows, blank_invalid_rows]:
                for index in df.index:
                    adderror(DATA.at[index, 'record'],column,DATA.at[index, column] if df is range_invalid_rows else 'Blank value not allowed','Out of range' if df is range_invalid_rows else 'Blank not allowed')

        elif question.type == 'text':
            # Text length checks
            if txt_min_length is not None or txt_max_length is not None:
                for index, value in DATA[column].dropna().iteritems():
                    cleaned_text = re.sub(r'[\s\W]+', '', str(value))
                    if (txt_min_length is not None and len(cleaned_text) < txt_min_length) or \
                       (txt_max_length is not None and len(cleaned_text) > txt_max_length):
                            adderror(DATA.at[index, 'record'],column,value,f'Text length violation (cleaned length {len(cleaned_text)})')


    # Completeness check if required
    if required == 1 and not DATA[question.datacols].notna().any(axis=1).any():
        for index in DATA.index:
            adderror(DATA.at[index, 'record'],question.id,"",f'Required response check failed')
