import numpy as np
import re
from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions
from logs import adderror
import pandas as pd
import numpy as np
from typing import List, Union, Callable, Optional, Tuple
# Define a type alias for range tuples
RangeTuple = Tuple[Union[int, float], Union[int, float]]

def checkTerm(term_label:str,condition: Callable):

    filtered_data = DATA[DATA.apply(condition, axis=1)]
    for index in filtered_data.index:
        adderror(filtered_data.at[index, 'record'], term_label, "", f'Term Check failed')
