import os
import pandas as pd
from logs import adderror
from config import *
from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank  
def checkmaxdiff(datarow, maxdiffdesign:pd.DataFrame, maxdiffq, hattrq, no_tasks, no_options, version,row_headers=[],loop_prefix=1,condition=True):
    """
    Validate MaxDiff data for each task in a given row of data.

    Parameters:
    -----------
    row : pd.Series
        The current row of data being validated.
    
    maxdiffdesignflecsv : str
        Path to the MaxDiff design file (CSV format).
    
    maxdiffQs : List[str]
        List of column names for MaxDiff questions.
    
    hAttrQ : str
        The base string of hAttrQ to be used in column names for attributes.

    row_headers: Array of desgign file columns
    loop_prefix: if ==1 then considers the loopprefix as "_Lr" otherwise "_"
    
    no_tasks : int
        The number of MaxDiff tasks to be validated.
    
    NofOpts : int
        Number of options for each task.
    
    version : str
        Version identifier to locate the correct design in the design file.
    
    Returns:
    --------
    None
        Logs errors via `adderror` if validation fails.

    """
    if condition:
        rslt_df = maxdiffdesign.loc[(maxdiffdesign['Version']==version)]
        for task in range(1, no_tasks + 1):
            if loop_prefix==1:
                mostcol = f"{maxdiffq}_Lr{task}c1"
                leastcol = f"{maxdiffq}_Lr{task}c2"
            else:
                mostcol = f"{maxdiffq}_{task}c1"
                leastcol = f"{maxdiffq}_{task}c2"

            itemArr=[rslt_df.iloc[task-1][each] for each in row_headers]  
            if loop_prefix==1:
                hAttr_rows=[f"{hattrq}_Lr{task}r{opt}" for opt in range(1, len(row_headers)+1)]
            else:
                hAttr_rows=[f"{hattrq}_{task}r{opt}" for opt in range(1, len(row_headers)+1)]
            
            # Validate each option based on hAttrQ
            for each in range(1, len(row_headers)+1):
                if datarow[hAttr_rows[each-1]] != itemArr[each-1]:  # Check if each attribute matches the design
                    adderror(datarow['record'], maxdiffq, task,f"MaxDiff design error for option")

            if datarow[mostcol]==datarow[leastcol]:
                adderror(datarow['record'],"Same response selected in max-diff iteration.")
            if (datarow[mostcol] not in itemArr) or (datarow[leastcol] not in itemArr):
                adderror(datarow['record'],"Max-diff values not in design.")
    else:
        for task in range(1,no_tasks + 1):
            if loop_prefix==1:
                mostcol = f"{maxdiffq}_Lr{task}c1"
                leastcol = f"{maxdiffq}_Lr{task}c2"
            else:
                mostcol = f"{maxdiffq}_{task}c1"
                leastcol = f"{maxdiffq}_{task}c2"

            if loop_prefix==1:
                hAttr_rows=[f"{hattrq}_Lr{task}r{opt}" for opt in range(1, no_options + 1)]
            else:
                hAttr_rows=[f"{hattrq}_{task}r{opt}" for opt in range(1, no_options + 1)]

            for each in hAttr_rows:
                if isnotblank(datarow[each]):
                    adderror(datarow['record'],"Max-diff hidden question blank check failed.")                

            if isnotblank(datarow[mostcol]) or isnotblank(datarow[leastcol]):
                adderror(datarow['record'],"Max-diff blank check failed.")
