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

    if len(error_df) > 0:
        grouped_df = error_df.groupby(['Reason', 'Column']).agg(
            Record=('Record', list),
            Count=('Record', 'count')
        ).reset_index()
        
        print(grouped_df)
        grouped_df.to_excel("./data/errors.xlsx", index=False)
    else:
        print("***NO ERRORS***")
