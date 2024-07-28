from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from logs import Error, ErrorLog

import pandas as pd

def checkrank(df, question, max_rank_type='static', max_rank_value=None, exclude_cols=[]):
    """
    Check for unique values across specified columns in a DataFrame, ensuring each value is present only once
    and falls within the specified dynamic rank range (min_rank = 1).

    Parameters:
    df (pd.DataFrame): The DataFrame to check.
    question (object): The question object containing datacols attribute (list of columns to check).
    max_rank_type (str): Type of max rank ('static', 'sum_columns', 'column').
    max_rank_value (int, list, str): Max rank value depending on max_rank_type.
                                     - 'static': integer
                                     - 'sum_columns': list of columns to sum for max rank
                                     - 'column': column name containing the max rank
    exclude_cols (list): List of columns to exclude from checking.

    Returns:
    pd.Series: Boolean series indicating if the values are unique and within the rank range for each row.
    """
    min_rank = 1

    # Filter out the columns to exclude
    columns_to_check = [col for col in question.datacols if col not in exclude_cols]

    # Determine max_rank for each row based on max_rank_type
    if max_rank_type == 'static':
        if not isinstance(max_rank_value, int):
            raise ValueError("For 'static' max_rank_type, max_rank_value must be an integer.")
        max_rank = pd.Series([max_rank_value] * len(df), index=df.index)
    elif max_rank_type == 'sum_columns':
        if not isinstance(max_rank_value, list) or not all(col in df.columns for col in max_rank_value):
            raise ValueError("For 'sum_columns' max_rank_type, max_rank_value must be a list of valid column names.")
        max_rank = df[max_rank_value].sum(axis=1)
    elif max_rank_type == 'column':
        if not isinstance(max_rank_value, str) or max_rank_value not in df.columns:
            raise ValueError("For 'column' max_rank_type, max_rank_value must be a valid column name.")
        max_rank = df[max_rank_value]
    else:
        raise ValueError("Invalid max_rank_type. Expected 'static', 'sum_columns', or 'column'.")

    # Function to check if values are unique and within the rank range for a single row
    def check_row(row, max_rank_val):
        values = row[columns_to_check].dropna().unique()  # Drop NaN values and get unique values
        if len(values) != row[columns_to_check].dropna().size:
            return False  # Values are not unique
        
        # Convert values to integers and check if they are within the rank range
        try:
            int_values = list(map(int, values))
        except ValueError:
            return False  # Non-integer values found

        return all(min_rank <= val <= max_rank_val for val in int_values)

    # Apply the check_row function to each row with corresponding max_rank value
    return df.apply(lambda row: check_row(row, max_rank.loc[row.name]), axis=1)

data = {
    'A': [1, 2, 3, None],
    'B': [4, 5, 6, None],
    'C': [7, 8, 9, 1],
    'D': [10, 11, 12, 13],
    'MaxRank': [15, 15, 15, 10]
}
df = pd.DataFrame(data)
question = QUESTIONS.q1


# Check with static max_rank
print(checkrank(df, question, max_rank_type='static', max_rank_value=15))

# Check with max_rank from another column
print(checkrank(df, question, max_rank_type='column', max_rank_value='MaxRank'))

# Check with max_rank as the sum of other columns
print(checkrank(df, question, max_rank_type='sum_columns', max_rank_value=['A', 'B']))

# Check with excluding some columns
print(checkrank(df, question, max_rank_type='static', max_rank_value=15, exclude_cols=['D']))

