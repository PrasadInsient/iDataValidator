import pandas as pd
from logs import adderror
from typing import List
from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank

def checkcompselection(
    question_id: str,
    data_row: pd.Series,
    familiarity_cols: List[str],
    ignore_cols: List[str] = [],
    comp1=None,
    comp2=None,
    comp3=None,
    comp4=None,
    priority_codes: List[int] = [],
    qual_order: List[int] = [1, 2, 3],
    priority_codes_qual_vals: List[int] = [1, 2, 3],
    condition: bool = True
):
    """
    Check the component selection based on priority codes and familiarity columns.

    Parameters:
    question_id (str): The question identifier.
    data_row (pd.Series): A pandas series representing a single row of data.
    familiarity_cols (List[str]): List of familiarity columns to check.
    ignore_cols (List[str]): Columns to be excluded from checking.
    comp1, comp2, comp3, comp4: Components to be checked.
    priority_codes (List[int]): List of priority codes for qualification.
    qual_order (List[int]): List defining the order of qualification levels.
    priority_codes_qual_vals (List[int]): Valid values for priority codes.
    condition (bool): A condition to determine whether the check should be applied.
    """
    if condition:
        # Initialize dictionaries to hold codes and track checked components
        codes = {1: [], 2: [], 3: [], 4: [], 5: []}
        priority_codes_qualified = []
        comps = [comp1, comp2, comp3, comp4]
        checked_comps = [False] * len(comps)
        non_zero_comps = [comp for comp in comps if comp not in (None, 0)]

        required = len(non_zero_comps)

        # Check if all non-zero comps are unique
        if required != len(set(non_zero_comps)):
            adderror(data_row['record'], question_id, "", "Duplicate comp selection error")
            return

        # Populate the codes dictionary and qualified priority codes
        for index, column in enumerate(familiarity_cols):
            if isnotblank(data_row[column]) and column not in ignore_cols:
                value = int(data_row[column])
                if (index + 1) in priority_codes and value in priority_codes_qual_vals:
                    priority_codes_qualified.append(index + 1)
                else:
                    codes[value].append(index + 1)

        prio_count = 0  # To track how many comps have been checked against priority codes

        # Validate comps against priority codes
        if priority_codes_qualified:
            for i, comp in enumerate(comps):
                if comp in (None, 0):
                    continue  # Skip zero or None comps

                if prio_count < required:
                    if comp not in priority_codes_qualified:
                        adderror(data_row['record'], question_id, comp, f"Comp{i+1} - Priority brand selection error")
                        return
                    else:
                        priority_codes_qualified.remove(comp)
                        checked_comps[i] = True
                        prio_count += 1
                        if not priority_codes_qualified:
                            break

        remaining = required - prio_count
        if remaining == 0:
            return  # All comps are valid

        # Helper function to check remaining comps in codes
        def check_remaining_comps(codes_level):
            nonlocal remaining
            sel_codes = codes[codes_level]
            if not sel_codes:
                return False  # Nothing to check

            for i, comp in enumerate(comps):
                if checked_comps[i]:
                    continue  # Already checked comp

                if comp is not None and comp in sel_codes:
                    sel_codes.remove(comp)
                    checked_comps[i] = True
                    remaining -= 1

                    if remaining == 0:
                        return True  # All comps are resolved
                    if not sel_codes:
                        return False

                elif comp is not None and comp not in sel_codes:
                    adderror(data_row['record'], question_id, comp, f"Comp{i+1} selection error")
                    return

            return False

        # Check remaining comps against the qualification order
        for level in qual_order:
            if check_remaining_comps(level):
                return

        # Final check if there are unresolved comps
        if remaining > 0:
            adderror(data_row['record'], question_id, "", "Not enough valid selections for comps")