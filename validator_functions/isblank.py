import pandas as pd
def isblank(val):
    return str(val) == "False" or pd.isna(val)