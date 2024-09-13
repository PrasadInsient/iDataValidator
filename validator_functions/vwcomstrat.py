import pandas as pd
from logs import adderror
from typing import List, Union, Tuple, Optional

RangeTuple = Tuple[Union[int, float], Union[int, float]]
def checkcomstrat(datarow: pd.Series, comstrat_qid_cols: List[str],masking_cols: List[str],range_param: RangeTuple =(1, 7),condition=True):
    if condition:
        no_of_cols=len(masking_cols)
        datacols_2d=[comstrat_qid_cols[i:i + no_of_cols] for i in range(0, len(comstrat_qid_cols), no_of_cols)]
        for eachArr in datacols_2d:
            for index, each in enumerate(masking_cols):
                if datarow[each]==1:
                    if datarow[eachArr[index]] not in range_param:
                        adderror(datarow['record'], eachArr[index], datarow[eachArr[index]], 'Invalid Value')
                else:
                    if not pd.isnull(datarow[eachArr[index]]):
                        adderror(datarow['record'], eachArr[index], datarow[eachArr[index]], 'Blank check failed')
    else:
        for each in comstrat_qid_cols:
            if not pd.isnull(datarow[each]):
                adderror(datarow['record'], each, datarow[each], 'Blank check failed')
