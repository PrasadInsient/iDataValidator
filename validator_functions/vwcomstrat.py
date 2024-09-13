import pandas as pd
from logs import adderror
from typing import List, Union, Tuple, Optional

RangeTuple = Tuple[Union[int, float], Union[int, float]]

def checkcomstrat(
    datarow: pd.Series, 
    comstrat_qid_cols: List[str], 
    masking_cols: List[str], 
    range_param: RangeTuple = (1, 7), 
    condition: bool = True
) -> None:
    """
    Checks a strategy compliance for a given data row.

    Parameters:
    -----------
    datarow : pd.Series
        A pandas Series representing a row of data.
    comstrat_qid_cols : List[str]
        List of column names representing the compliance strategy question IDs.
    masking_cols : List[str]
        List of column names representing the masking strategy.
    range_param : Tuple[Union[int, float], Union[int, float]], optional
        A tuple specifying the valid range for the compliance strategy values, default is (1, 7).
    condition : bool, optional
        A condition to control whether to apply the masking strategy, default is True.

    Returns:
    --------
    None
        The function logs errors using `adderror` if the compliance strategy checks fail.

    Errors:
    -------
    - Logs an 'Invalid Value' error if a masked column is 1 but the value in the corresponding compliance strategy column is not in the valid range.
    - Logs a 'Blank check failed' error if the value in a compliance strategy column is not blank where it should be.

    """
    if condition:
        no_of_cols = len(masking_cols)
        datacols_2d = [comstrat_qid_cols[i:i + no_of_cols] for i in range(0, len(comstrat_qid_cols), no_of_cols)]
        for eachArr in datacols_2d:
            for index, each in enumerate(masking_cols):
                if datarow[each] == 1:
                    if datarow[eachArr[index]] not in range_param:
                        adderror(datarow['record'], eachArr[index], datarow[eachArr[index]], 'Invalid Value')
                else:
                    if not pd.isnull(datarow[eachArr[index]]):
                        adderror(datarow['record'], eachArr[index], datarow[eachArr[index]], 'Blank check failed')
    else:
        for each in comstrat_qid_cols:
            if not pd.isnull(datarow[each]):
                adderror(datarow['record'], each, datarow[each], 'Blank check failed')
