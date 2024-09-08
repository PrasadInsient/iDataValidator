import pandas as pd
from logs import adderror
from typing import List

def checkcompselection(
    questionid: str,
    datarow: pd.Series,
    familaritycols: List[str],
    exclude_cols: List[str] = [],
    comp1=None,
    comp2=None,
    comp3=None,
    comp4=None,
    order=[1, 2, 3],
    priporitycodes=[],
    condition: bool = True
):
    if condition:
        codes = {1: [], 2: [], 3: [], 4: [], 5: []}  # Dictionary to store codes1-codes5
        prioritycodes_qualified = []
        comps = [comp1, comp2, comp3, comp4]
        checked_comps = [False, False, False, False]  # To track which comps have been checked
        non_zero_comps = [comp for comp in comps if comp is not None and comp != 0]

        # Ensure all non-zero comps are unique
        if len(non_zero_comps) != len(set(non_zero_comps)):
            adderror(datarow['record'], questionid, "", "Duplicate comp selection error")
            return

        # Fill the codes1-codes5 and qualified priority codes
        for index, column in enumerate(familaritycols):
            if pd.notna(datarow[column]) and column not in exclude_cols:
                value = int(datarow[column])  # Assuming integer values
                if index + 1 in priporitycodes and value in order:
                    prioritycodes_qualified.append(index + 1)
                else:
                    codes[value].append(index + 1)

        # Check comps against priority codes
        prio_index = 0  # This keeps track of the current priority code being used
        for i, comp in enumerate(comps):
            if comp == 0 or comp is None:
                continue  # Skip zero comps
            if prio_index < len(prioritycodes_qualified):
                if comp != prioritycodes_qualified[prio_index]:
                    checked_comps[i] = True
                    adderror(datarow['record'], questionid, comp, f"Comp{i+1} selection error")
                prio_index += 1

        remaining = len(non_zero_comps) - prio_index
        if remaining == 0: return

        # Function to check comps in codes1-codes5 based on remaining comps
        def check_remaining_comps(codes_level):
            nonlocal remaining
            for i, comp in enumerate(comps):
                if not checked_comps[i] and comp != 0 and comp not in codes[codes_level]:
                    checked_comps[i] = True
                    remaining -= 1
                    adderror(datarow['record'], questionid, comp, f"Comp{i+1} selection error")
            return remaining == 0

        # Check comps in codes based on the order
        for level in order:
            if check_remaining_comps(level):
                return

        # If remaining comps couldn't be resolved
        if remaining > 0:
            adderror(datarow['record'], questionid, "", "Not enough valid selections for comps")
