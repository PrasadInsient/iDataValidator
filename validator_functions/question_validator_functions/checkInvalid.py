import numpy as np
import re
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror
import pandas as pd
import numpy as np
from typing import List, Union, Callable, Optional, Tuple
# Define a type alias for range tuples
RangeTuple = Tuple[Union[int, float], Union[int, float]]

def qinvalidate_single_multiple(datacols, data, invalid_values,blank_as_invalid):
    for column in datacols:
        if callable(invalid_values):
            data['invalid_values'] = data.apply(lambda row: invalid_values(row), axis=1)
        else:
            data['invalid_values'] = [invalid_values] * len(data)

        data['invalid_values'] = data['invalid_values'].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

        invalid_rows = data[
            data.apply(
                lambda row: (
                    (blank_as_invalid and pd.isnull(row[column])) or
                    (not pd.isnull(row[column]) and row[column] in row['invalid_values'])
                ),
                axis=1
            )
        ]

        for index in invalid_rows.index:
            adderror(data.at[index, 'record'], column, data.at[index, column], 'Invalid Value')

def qinvalidate_number(datacols, data, range_param,blank_as_invalid):
    for column in datacols:
        if callable(range_param):
            data['range_limits'] = data.apply(lambda row: range_param(row), axis=1)
        else:
            data['range_limits'] = [range_param] * len(data)
        
        range_invalid_rows = data[
            data.apply(
                lambda row: (
                    (blank_as_invalid and pd.isnull(row[column])) or
                    (not pd.isnull(row[column]) and (row['range_limits'][0] <= row[column] <= row['range_limits'][1]))
               ),
               axis=1
            )
        ]

        for index in range_invalid_rows.index:
            adderror(data.at[index, 'record'], column, data.at[index, column], 'Invalid Value - Out of range')

def checkInvalid(
    datacols: List[str],
    columns_type:str="single",
    invalid_values: Union[List, Callable, np.ndarray] = [0, 1],
    blank_as_invalid=True,
    exclude_cols: List[str] = [],
    invalid_range_value: Union[RangeTuple, Callable[[pd.Series], RangeTuple]] = (0, 100),
    condition: Optional[Callable] = None,
):
    if condition is None:
        condition = lambda x: True

    # Create a filtered DataFrame based on the condition
    filtered_data = DATA[DATA.apply(condition, axis=1)]
    datacols = [col for col in datacols if col not in exclude_cols]
    
    if columns_type in ['single', 'multiple']:
        qinvalidate_single_multiple(datacols,filtered_data, invalid_values,blank_as_invalid)
    elif columns_type == 'number':
        qinvalidate_number(datacols, filtered_data, invalid_range_value,blank_as_invalid)