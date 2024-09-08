import os
import pandas as pd
from logs import adderror
from config import *
def checkmaxdiff(datarow, maxdiffdesignflecsv, maxdiffQs, hAttrQ, no_tasks, NofOpts, version,condition):
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

    # Load the design file into a DataFrame
    designfile_path = os.path.join(BASE_DIR, 'data', maxdiffdesignflecsv)
    df_design_maxdiff = pd.read_csv(designfile_path)

    for task in range(1, no_tasks + 1):
        mxq1 = maxdiffQs[(task-1) * 2]  # First question column for the task
        mxq2 = maxdiffQs[((task-1)*2) + 1]  # Second question column for the task

        # Check if the two MaxDiff columns have the same values
        if datarow[mxq1] == datarow[mxq2]:
            adderror(datarow['record'], mxq1,task,f"MaxDiff columns have the same value")

        # Get the design values for this task
        codeNum = f"{version}_{task}"
        listX = df_design_maxdiff[codeNum].iloc[0].split("#")  # Get the design options as a list
        listX = [int(item) for item in listX]  # Convert the design list to integers

        # Check if the values in MaxDiff columns are valid according to the design
        if (datarow[mxq1] not in listX) or (datarow[mxq2] not in listX):
            adderror(datarow['record'], mxq1, task, f"MaxDiff columns contain invalid values")

        # Validate each option based on hAttrQ
        for opt in range(1, NofOpts + 1):
            attr_col = f"{hAttrQ}_{task}r{opt}"
            if datarow[attr_col] != listX[opt - 1]:  # Check if each attribute matches the design
                adderror(datarow['record'], mxq1, task,f"MaxDiff design error for option")

