import pandas as pd
from logs import adderror
from typing import List, Union, Tuple, Optional

def checkcomstrat(
    valid_values: list,
    datarow: pd.Series, 
    comstrat_qid_cols: List[str], 
    masking_cols: List[str], 
    condition: bool = True
) -> None:
    """
    Checks a comstrat question for a given data row.

    Parameters:
    -----------
    datarow : pd.Series
        A pandas Series representing a row of data.
    comstrat_qid_cols : List[str]
        List of starrating question columns (please make sure this works only if grouping=Cols is not mentioned in the question).
    masking_cols : List[str]
        List of masking multi question columns.
    range_param : Tuple[Union[int, float], Union[int, float]], optional
        A tuple specifying the valid range for the compliance strategy values, default is (1, 7).
    condition : bool, optional
        A condition to control whether to apply the masking strategy, default is True.

    checkcomstrat(
    datarow: row, 
    comstrat_qid_cols: [QUESTIONS.Comstrat.datacols], 
    masking_cols: [QUESTIONS.hComstrat.datacols], 
    range_param: np.arange(1,7), 
    condition: bool = True
)
    """
    
    if condition:
        no_of_cols = len(masking_cols)
        #datacols_2d -- is 2d list with list for each attribute 
        datacols_2d = [comstrat_qid_cols[i:i + no_of_cols] for i in range(0, len(comstrat_qid_cols), no_of_cols)]
        #Loop through each attribute list 
        for eachArr in datacols_2d:
            for index, each in enumerate(masking_cols):
                if datarow[each] == 1:
                    if datarow[eachArr[index]] not in valid_values:
                        adderror(datarow['record'], eachArr[index], datarow[eachArr[index]], 'Invalid Value')
                else:
                    if not pd.isnull(datarow[eachArr[index]]):
                        adderror(datarow['record'], eachArr[index], datarow[eachArr[index]], 'Blank check failed')
    else:
        for each in comstrat_qid_cols:
            if not pd.isnull(datarow[each]):
                adderror(datarow['record'], each, datarow[each], 'Blank check failed')
