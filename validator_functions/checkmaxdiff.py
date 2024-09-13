import os
import pandas as pd
from logs import adderror
from config import *
def checkmaxdiff(datarow, maxdiffdesign, maxdiffq, hattrq, no_tasks, no_options, version,condition):
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
    if condition:
        # Load the design file into a DataFrame
        designfile_path = os.path.join(BASE_DIR, 'data', maxdiffdesign)
        df_design_maxdiff = pd.read_csv(designfile_path)

        for task in range(1, no_tasks + 1):
            mostcol = f"{maxdiffq}_Lr{task}c1"
            leastcol = f"{maxdiffq}_Lr{task}c2"

            # Check if the two MaxDiff columns have the same values
            if datarow[mostcol] == datarow[leastcol]:
                adderror(datarow['record'], maxdiffq,task,f"MaxDiff columns have the same value")

            # Get the design values for this task
            codeNum = f"{version}_{task}"
            listX = df_design_maxdiff[codeNum].iloc[0].split("#")  # Get the design options as a list
            listX = [int(item) for item in listX]  # Convert the design list to integers

            # Check if the values in MaxDiff columns are valid according to the design
            if (datarow[mostcol] not in listX) or (datarow[leastcol] not in listX):
                adderror(datarow['record'], maxdiffq, task, f"MaxDiff columns contain invalid values")

            # Validate each option based on hAttrQ
            for opt in range(1, no_options + 1):
                attr_col = f"{hattrq}_Lr{task}{opt}"
                if datarow[attr_col] != listX[opt - 1]:  # Check if each attribute matches the design
                    adderror(datarow['record'], maxdiffq, task,f"MaxDiff design error for option")