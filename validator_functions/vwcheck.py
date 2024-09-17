import pandas as pd
from logs import adderror
from typing import List, Union, Tuple, Optional
from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank  

class Question:
    def __init__(self,id, type, parent_record,datacols=[],oecols=[]):
        self.id:str = id
        self.type:str = type
        self.datacols:List[str] = datacols
        self.oecols:List[str] = oecols
        self.parent_record = parent_record

RangeTuple = Tuple[Union[int, float], Union[int, float]]


def slice_columns(question, num_elements):
    """
    Slice the datacols into sublists of size num_elements in sequence order.
    """
    datacols = question.datacols
    return [datacols[i:i + num_elements] for i in range(0, len(datacols), num_elements)]

def vwcheck(datarow: pd.Series, VW_questions: List[Question], range_param: RangeTuple = (0, 100),  OrderType: int = 1, condition: bool = True,maskQIDvalue: int = 1, maskingQID: Optional[Question] = None):
    """
    
    vwcheck(datarow, [QUESTION.VW_acc,QUESTION.VW_exce,QUESTION.VW_tooexc,QUESTION.VW_toocheep], range_param=(50, 100))


    Validates the VW (Value for Money) check based on the specified questions and columns.
    Slices the `vw_data` lists (e.g., vw_data1, vw_data2) into sublists based on the number of columns 
    and applies VW logic, including range checks, column masking, and order validation.

    Parameters:
        datarow (pd.Series): A row from a pandas DataFrame representing the current data being validated.
        
           Example Usage:
        # Example datarow from a DataFrame
        datarow = pd.Series({
            'record': '001',
            'too_cheap': 50,
            'affordable': 100,
            'expensive': 150,
            'too_expensive': 200
        })
        
        VW_questions (list): A list of `Question` objects representing the VW columns for each question. 
                             Each question contains `datacols` with relevant column data for the check. Pass all VW questions in sequence order.
        range_param (tuple): A tuple specifying the valid range (min, max) for numeric VW question values.
        OrderType (int): Specifies the order validation type. Default `1` represents the order 
                         'Acceptable > Expensive > Too Expensive > Too Cheap'. (too cheep only if applecable) 
                         If set to `2`, the order is reversed: 'Too Cheap > Acceptable > Expensive > Too Expensive'.
        condition (bool): A flag to enable or disable the check. If True, performs the VW check. If False, checks that all datacols are not null.
                          Default is True.
        maskQIDvalue (int): The threshold value for `maskingQID` that determines whether a VW column should be checked. 
                            Applicable only when `maskingQID` is present. For column masking from a multi question, it works as-is. 
                            For masking from numeric question, only columns with values greater than or equal to this threshold are checked.
        maskingQID (Optional[Question]): An optional masking question used for column masking in multi-column VW checks.
                                         If provided, it determines whether a specific column is checked.
    """


    # Number of columns is determined from the first question
    num_cols = len(VW_questions[0].datacols)

    # Create empty vw_data lists for each question
    vw_data = []

    # Populate vw_data lists by slicing the datacols into sublists
    for i, question in enumerate(VW_questions):
        num_elements = i + 1  # Number of elements per slice depends on question index
        vw_data.append(slice_columns(question, num_elements))

    if condition:
        # Loop through each column index
        for col_idx in range(num_cols):
            # Iterate over each vw_data group
            for i, data_group in enumerate(vw_data):
                col_data = data_group[col_idx] if col_idx < len(data_group) else []

                if maskingQID:
                    mask_value = datarow[maskingQID.datacols[col_idx]]
                    if mask_value < maskQIDvalue:
                        if any(not pd.isnull(datarow[col]) for col in col_data):
                            adderror(datarow['record'], col_idx, col_data, "VW blank check failed.")
                        continue

                # Range check for each column's data
                if not all(range_param[0] <= datarow[val] <= range_param[1] for val in col_data if not pd.isnull(datarow[val])):
                    adderror(datarow['record'], col_idx, col_data, f"Value out of range: {range_param}")

                if any(pd.isnull(datarow[col]) for col in col_data):
                    adderror(datarow['record'], col_idx, col_data, "VW data have blanks.")

                    
                # For the last question, check if the order is correct
                if i == len(VW_questions) - 1:
                    # Perform the order validation based on OrderType
                    for k in range(len(col_data) - 1):
                        if OrderType == 2 or len(VW_questions)<4:
                            # Ensure increasing order
                            if datarow[col_data[k]] >= datarow[col_data[k + 1]]:
                                adderror(datarow['record'], col_data[k], datarow[col_data[k]], "VW check failed.")
                        else:
                            # Ensure vw order (last < first)
                            if k == len(col_data) - 2:
                                if datarow[col_data[k + 1]] >= datarow[col_data[0]]:
                                    adderror(datarow['record'], col_data[k + 1], datarow[col_data[k + 1]], "VW check failed.")
                            else:
                                if datarow[col_data[k]] >= datarow[col_data[k + 1]]:
                                    adderror(datarow['record'], col_data[k], datarow[col_data[k]], "VW check failed.")

    
            # Cross-check logic for data columns between vw_data lists
            # Cross-check first data column between vw_data[0], vw_data[1], vw_data[2], vw_data[3] (if applicable)
            for i in range(1, len(vw_data)):
                if len(vw_data[i]) > 0 and len(vw_data[0]) > 0:
                    first_data_col_vw1 = vw_data[0][col_idx] if col_idx < len(vw_data[0]) else []
                    first_data_col_vw2 = vw_data[i][col_idx] if col_idx < len(vw_data[i]) else []
                    if not all(datarow[d1] == datarow[d2] for d1, d2 in zip(first_data_col_vw1, first_data_col_vw2) if not pd.isnull(datarow[d1]) and not pd.isnull(datarow[d2])):
                        adderror(datarow['record'], col_idx, first_data_col_vw1, "Mismatch in first data column across questions")

            # Cross-check second data column between vw_data[1] and vw_data[2], vw_data[3] (if applicable)
            if len(vw_data) > 2:
                for i in range(2, len(vw_data)):
                    if len(vw_data[i]) > 1 and len(vw_data[1]) > 1:
                        second_data_col_vw2 = vw_data[1][col_idx] if col_idx < len(vw_data[1]) else []
                        second_data_col_vw3 = vw_data[i][col_idx] if col_idx < len(vw_data[i]) else []
                        if not all(datarow[d2] == datarow[d3] for d2, d3 in zip(second_data_col_vw2, second_data_col_vw3) if not pd.isnull(datarow[d2]) and not pd.isnull(datarow[d3])):
                            adderror(datarow['record'], col_idx, second_data_col_vw2, "Mismatch in second data column across questions")

            # Cross-check third data column between vw_data[2] and vw_data[3] (if applicable)
            if len(vw_data) > 3:
                if len(vw_data[2]) > 2 and len(vw_data[3]) > 2:
                    third_data_col_vw3 = vw_data[2][col_idx] if col_idx < len(vw_data[2]) else []
                    third_data_col_vw4 = vw_data[3][col_idx] if col_idx < len(vw_data[3]) else []
                    if not all(datarow[d3] == datarow[d4] for d3, d4 in zip(third_data_col_vw3, third_data_col_vw4) if not pd.isnull(datarow[d3]) and not pd.isnull(datarow[d4])):
                        adderror(datarow['record'], col_idx, third_data_col_vw3, "Mismatch in third data column across questions")

    else:
        # Check if all datacols are not null
        for question in VW_questions:
            if any(not pd.isnull(datarow[col]) for col in question.datacols):
                adderror(datarow['record'], None, None, "VW blank check failed.")
