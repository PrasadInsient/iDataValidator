import re
import pandas as pd
from logs import adderror

def validatetext(questionid, datacols, datarow:pd.Series, optional_cols=[],exclusive_cols=[],ignore_cols=[],
                 at_least=1, at_most=-1,txt_mnlen=1,txt_mxlen=None,allowblanks=False,required=1,condition=True):
    datarow = datarow.copy()

    for col in exclusive_cols:
        if col not in datacols: datacols.append(col)

    for col in ignore_cols:
        if col not in datacols: datacols.remove(col)

    if condition:
        no_selections=0
        no_exclusive_selections=0
        no_non_exclusive_selections=0

        for column in datacols:
            if column not in exclusive_cols:
                allowcolumnnblank = allowblanks or column in optional_cols
                if (not allowcolumnnblank and pd.isnull(datarow[column])):
                    adderror(datarow['record'], column, datarow[column], 'Invalid Value')
                else:
                    if pd.notnull(datarow[column]):
                        cleaned_text = re.sub(r'[\s\W]+', '', str(datarow[column]))
                        if (txt_mnlen is not None and len(cleaned_text) < txt_mnlen) or \
                            (txt_mxlen is not None and len(cleaned_text) > txt_mxlen):
                            adderror(datarow['record'], column, datarow[column], 'Invalid Value')
            if pd.notnull(datarow[column]):
                no_selections=no_selections+1
                if column in exclusive_cols:
                    no_exclusive_selections=no_exclusive_selections+1
                else:
                    no_non_exclusive_selections += 1

        if required and no_selections==0:
            adderror(datarow['record'], questionid, no_selections, 'Text at least 1 check failed.')
        elif required:
            if no_exclusive_selections==0 and at_least>1 and no_selections<at_least:
                adderror(datarow['record'], questionid, no_selections, 'Text at least N check failed.')
            if no_exclusive_selections==0 and at_most>1 and no_selections>at_most:
                adderror(datarow['record'], questionid, no_selections, 'Text at most N check failed.')
        if no_non_exclusive_selections>0 and no_exclusive_selections>0:
            adderror(datarow['record'], questionid, no_selections, 'Text exclusive check failed.')

    else:
        for column in datacols:
            if not pd.isnull(datarow[column]):
                adderror(datarow['record'], questionid, datarow[column], 'Blank check failed')
