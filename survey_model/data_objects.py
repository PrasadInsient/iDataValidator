import pandas as pd
from .columns import Columns
from .questions import Questions
from .questiontypes import QuestionTypes

def convert_column(column):
    # Check if the column can be converted to Int64
    try:
        # Drop NaN values and check if the remaining are integers
        if pd.Series(column.dropna()).apply(lambda x: float(x).is_integer()).all():
            return column.astype('Int64')
        else:
            return column
    except ValueError:
        return column

DATA:pd.DataFrame= pd.DataFrame()

for column in DATA.columns:
    DATA[column] = convert_column(DATA[column])

COLUMNS = Columns()
QUESTIONS = Questions()
QUESTIONTYPES = QuestionTypes()