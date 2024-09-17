import pandas as pd
def isnotblank(val):
    return pd.notna(val) and str(val) != "False"

