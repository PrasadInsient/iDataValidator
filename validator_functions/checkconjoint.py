import os
import pandas as pd
import numpy as np
from logs import adderror
from config import *
from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank  

def checkconjoint(datarow, conjointdesign:pd.DataFrame,row_headers, conjointq, hattrq, no_tasks, no_options, version,condition):
    """
    Validates a respondent's conjoint data row against the predefined conjoint design.

    Parameters:
    -----------
    datarow : pd.Series
        A Pandas Series representing the respondent's data row with answers to the conjoint survey.
    
    conjointdesign : str
        Filename of the conjoint design CSV file, used to validate the respondent's answers.
    row_headers= List[str]
        Array of Column headers from the design file ex: ['Att 1','Att 2','Att 3','Att 4','Att 5','Att 6','Att 7']
    conjointq : str
        Conjoint Question id. Please pass without the Loopvar:label for ex: "Q_Conjoint"
    
    hattrq : str
        Hidden question ID for the conjoint attributes in the dataset. for ex: "hAttr", It will works only if we give attribute labels in 
        Sequential order.
    
    no_tasks : int
        Number of tasks/loops in the conjoint exercise (e.g., 12 tasks).
    
    no_options : int
        Number of possible options per screen (e.g., 4 options for each task).
    
    version : int
        The version of the conjoint survey design that the respondent was assigned.
    
    condition : bool
        Asking condition for the conjoint.
        
    Functionality:
    --------------
    - If `condition` is True:
        - It loads the conjoint design file and checks if the respondent's answers match the design.
        - Compares the respondent's answers for each task and attribute against the design.
        - Logs errors if any values are invalid or do not match the design for the given version.
    - If `condition` is False:
        - Checks if conjoint answers that should be left blank are indeed blank, logging an error if they are not.
    
    Raises:
    -------
    - Calls `adderror()` for any mismatches or invalid values found during validation.
    """
    if condition:        
        for x in range(1,no_tasks + 1):
            conjoint_qid1=conjointq+"_Lr"+str(x)
            conjoint_vals=[each for each in range(1,no_options+1)]
            if datarow[conjoint_qid1] not in conjoint_vals:
                adderror(datarow['record'], conjoint_qid1, x, f"conjoint contain invalid values")

        rslt_df1 = conjointdesign.loc[(conjointdesign['Version']==version) & (conjointdesign['Concept']==1)]
        rslt_df2 = conjointdesign.loc[(conjointdesign['Version']==version) & (conjointdesign['Concept']==2)]
        rslt_df3 = conjointdesign.loc[(conjointdesign['Version']==version) & (conjointdesign['Concept']==3)]
        rslt_df4 = conjointdesign.loc[(conjointdesign['Version']==version) & (conjointdesign['Concept']==4)]
        
        for loop in np.arange(1,no_tasks + 1):
            for index,rowheader in enumerate(row_headers):
                attr_colr1 = f"{hattrq}{index+1}_Lr{loop}r1"
                attr_colr2 = f"{hattrq}{index+1}_Lr{loop}r2"
                attr_colr3 = f"{hattrq}{index+1}_Lr{loop}r3"
                attr_colr4 = f"{hattrq}{index+1}_Lr{loop}r4"
                if rslt_df1.iloc[loop-1][rowheader]!=datarow[attr_colr1]: 
                    adderror(datarow['record'], attr_colr1, 0, f"conjoint task1 check failed.")

                if rslt_df2.iloc[loop-1][rowheader]!=datarow[attr_colr2]:
                    adderror(datarow['record'], attr_colr2, 0, f"conjoint task2 check failed.")

                if rslt_df3.iloc[loop-1][rowheader]!=datarow[attr_colr3]:
                    adderror(datarow['record'], attr_colr3, 0, f"conjoint task3 check failed.")

                if rslt_df4.iloc[loop-1][rowheader]!=datarow[attr_colr4]:
                    adderror(datarow['record'], attr_colr4, 0, f"conjoint task4 check failed.")
    else:
        for x in range(1,no_tasks + 1):
            conjoint_qid1=conjointq+"_Lr"+str(x) 
            if isnotblank(datarow[conjoint_qid1]): 
                adderror(datarow['record'], conjoint_qid1, x, f"conjoint blank check failed.")

  