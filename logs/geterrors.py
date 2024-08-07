from typing import List
import pandas as pd

from logs import *

def geterrors():
        # Convert ErrorLog to a DataFrame
    error_data = {
        "Record": [error.record for error in ErrorLog],
        "Column": [error.errorcolumn for error in ErrorLog],
        "Value": [error.errorvalue for error in ErrorLog],
        "Reason": [error.err_reason for error in ErrorLog]
    }

    error_df = pd.DataFrame(error_data)
    grouped_df = error_df.groupby(['Reason', 'Column', 'Value']).agg({'Record': ['list', 'count']}).reset_index()
    grouped_df.columns = ['Reason', 'Column', 'Value', 'Record', 'Count']
    if len(error_df)>0:
        print(grouped_df)
        grouped_df.to_excel("./data/errors.xlsx")
    else:
        print("***NO ERRORS***")