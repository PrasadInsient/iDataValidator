import pandas as pd
import numpy as np
from .columns import Columns
from .questions import Questions
from .questiontypes import QuestionTypes

def convert_column(column):
    # Replace any pd.NA with np.nan
    column = column.replace({pd.NA: np.nan})
    
    try:
        # Check if all non-NaN values are integers by verifying if x % 1 == 0 for each value
        if column.dropna().apply(lambda x: x % 1 == 0).all():
            # Convert the column to Int64 if all values are integers
            return column.astype('Int64')
        else:
            return column
    except (ValueError, TypeError):
        # If there's an error, return the original column without changes
        return column

DATA = pd.DataFrame()

for column in DATA.columns:
    DATA[column] = convert_column(DATA[column])

COLUMNS = Columns()
QUESTIONS = Questions()
QUESTIONTYPES = QuestionTypes()
