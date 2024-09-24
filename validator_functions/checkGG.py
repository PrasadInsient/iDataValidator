import pandas as pd
from logs import adderror
from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank

"""
Validates a respondent's GG data 

Parameters:
-----------
GGquestion : str
    GGquestion Question id. Please pass without the Loopvar:label for ex: "Q_GG"

datarow : pd.Series
    A Pandas Series representing the respondent's data row with answers to the conjoint survey.

GGprices : []]
    List of GG prices.    

priceq : str
    Hidden price question where we are punching the price that respondent is going to see.
    for ex: "hPrice_GG"    

start_pos : 3
    Starting position of the GG.    

no_times : As it is a two way GG the default number of time the GG asked will be 3 if we have 5 prices.

order: integer
# Update direction and price index based on selection and order.

condition : bool
    Asking condition for the GG.
    
"""

def checktwowayGG(GGquestion: str, datarow: pd.Series, GGprices=[], priceq: str = "",
                  start_pos=3, no_times=3, hideinvalidoptions=1, order=1, condition: bool = True):
    
    datarow = datarow.copy()
    
    if condition:    
        dir = 0
        status = 1
        priceindex = start_pos - 1
        
        for itr in range(1, no_times + 1):
            pricecol = f"{priceq}_Lr{itr}"
            GGqcol = f"{GGquestion}_Lr{itr}"
            if itr >1:
                pGGval = datarow[f"{GGquestion}_Lr{itr-1}"]
            
            if status == 1:
                valid_values = []
                if itr == 1 or hideinvalidoptions==0:
                    valid_values=[1,2,3,4,5]
                elif dir==1:
                    valid_values=range(1,pGGval+1)
                else:
                    valid_values=range(pGGval,6)

                price = GGprices[priceindex]
                GGselection = datarow[GGqcol]

                if price != datarow[pricecol]:
                    adderror(datarow['record'], GGquestion, datarow[pricecol], "GG - Price mismatch")
                    return

                if isblank(GGselection) or GGselection not in valid_values:
                    adderror(datarow['record'], GGquestion, datarow[GGqcol], "GG - Invalid value")
                    return

                # Update direction and price index based on selection and order
                if dir == 0:
                    if order==1:
                        dir = 1 if GGselection >= 3 else -1
                    else:
                        dir = -1 if GGselection >= 3 else 1

                if dir == 1: priceindex += 1
                else: priceindex -= 1
                
                # Check for status change to stop validation
                if order==1:
                    if (dir == 1 and GGselection == 1) or (dir == -1 and GGselection == 5):
                        status = 0
                else:
                    if (dir == 1 and GGselection == 5) or (dir == -1 and GGselection == 1):
                        status = 0

            else:
                if isnotblank(datarow[GGqcol]) or isnotblank(datarow[pricecol]):
                    adderror(datarow['record'], GGquestion, datarow[pricecol], "GG - Blank check failed")
                    return
    else:
        for itr in range(1, no_times + 1):
            pricecol = f"{priceq}_Lr{itr}"
            GGqcol = f"{GGquestion}_Lr{itr}"
            if isnotblank(datarow[GGqcol]) or isnotblank(datarow[pricecol]):
                adderror(datarow['record'], GGquestion, datarow[pricecol], "GG - Blank check failed")
                return

def checkonewayGG(GGquestion: str, datarow: pd.Series, GGprices=[], priceq: str = "",
                  start_pos=0, no_times=5, hideinvalidoptions=1, order=1,condition: bool = True):
    datarow = datarow.copy()
    if condition:
        dir = 1
        status = 1
        priceindex = start_pos - 1
        
        for itr in range(1, no_times + 1):
            pricecol = f"{priceq}_Lr{itr}"
            GGqcol = f"{GGquestion}_Lr{itr}"
            pGGval = datarow[f"{GGquestion}_Lr{itr-1}"]
            
            if status == 1:
                valid_values = []
                if itr == 1 or hideinvalidoptions==0:
                    valid_values=[1,2,3,4,5]
                elif dir==1:
                    valid_values=range(1,pGGval+1)
                else:
                    valid_values=range(pGGval,6)

                price = GGprices[priceindex]
                GGselection = datarow[GGqcol]

                if price != datarow[pricecol]:
                    adderror(datarow['record'], GGquestion, datarow[pricecol], "GG - Price mismatch")
                    return

                if isblank(GGselection) or GGselection not in valid_values:
                    adderror(datarow['record'], GGquestion, datarow[GGqcol], "GG - Invalid value")
                    return

                # Update direction and price index based on selection and order
                if dir == 0:
                    if order==1:
                        dir = 1 if GGselection >= 3 else -1
                    else:
                        dir = -1 if GGselection >= 3 else 1

                if dir == 1: priceindex += 1
                else: priceindex -= 1
                
                # Check for status change to stop validation
                if order==1:
                    if (dir == 1 and GGselection == 1) or (dir == -1 and GGselection == 5):
                        status = 0
                else:
                    if (dir == 1 and GGselection == 5) or (dir == -1 and GGselection == 1):
                        status = 0

            else:
                if isnotblank(datarow[GGqcol]) or isnotblank(datarow[pricecol]):
                    adderror(datarow['record'], GGquestion, datarow[pricecol], "GG - Blank check failed")
                    return
    else:
        for itr in range(1, no_times + 1):
            pricecol = f"{priceq}_Lr{itr}"
            GGqcol = f"{GGquestion}_Lr{itr}"
            if isnotblank(datarow[GGqcol]) or isnotblank(datarow[pricecol]):
                adderror(datarow['record'], GGquestion, datarow[pricecol], "GG - Blank check failed")
                return
                
