import os
import pandas as pd
from logs import adderror
from config import *
def checkconjoint(datarow, conjointdesign, conjointq, hattrq, no_tasks, no_options, version,condition):
    """
    Validate conjoint data for each task in a given row of data.

    Parameters:
    -----------
    row : pd.Series
        The current row of data being validated.
    
    conjointdesignflecsv : str
        Path to the conjoint design file (CSV format).
    
    conjointQs : List[str]
        List of column names for conjoint questions.
    
    hAttrQ : str
        The base string of hAttrQ to be used in column names for attributes.
    
    no_tasks : int
        The number of conjoint tasks to be validated.
    
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
        designfile_path = os.path.join(BASE_DIR, 'data', conjointdesign)
        df_design_conjoint = pd.read_csv(designfile_path)

        for task in range(1, no_tasks + 1):
            mostcol = f"{conjointq}_lr{task}c1"
            leastcol = f"{conjointq}_lr{task}c2"

            # Check if the two conjoint columns have the same values
            if datarow[mostcol] == datarow[leastcol]:
                adderror(datarow['record'], conjointq,task,f"conjoint columns have the same value")

            # Get the design values for this task
            codeNum = f"{version}_{task}"
            listX = df_design_conjoint[codeNum].iloc[0].split("#")  # Get the design options as a list
            listX = [int(item) for item in listX]  # Convert the design list to integers

            # Check if the values in conjoint columns are valid according to the design
            if (datarow[mostcol] not in listX) or (datarow[leastcol] not in listX):
                adderror(datarow['record'], conjointq, task, f"conjoint columns contain invalid values")

            # Validate each option based on hAttrQ
            for opt in range(1, no_options + 1):
                attr_col = f"{hattrq}_{task}r{opt}"
                if datarow[attr_col] != listX[opt - 1]:  # Check if each attribute matches the design
                    adderror(datarow['record'], conjointq, task,f"conjoint design error for option")