import pandas as pd
import numpy as np

from validator_functions.isblank import isblank
from validator_functions.isnotblank import isnotblank  

def checkcondition(value, condition: str) -> bool:
    """
    Checks if a given value satisfies a condition based on various operators such as '=', 'in', 'range', '>', '<', etc.

    Parameters:
        value (int/float): The value to be checked against the condition.
        condition (str): A string representing the condition to check against. Supported conditions include:
                         - '=': Equals (e.g., '=5' checks if value equals 5)
                         - 'in': In a list of values (e.g., 'in[1,2,3]' checks if value is 1, 2, or 3)
                         - 'range': Within a range (e.g., 'range(1,10)' checks if value is between 1 and 10, inclusive)
                         - '>': Greater than (e.g., '>5' checks if value is greater than 5)
                         - '<': Less than (e.g., '<10' checks if value is less than 10)
                         - '>=': Greater than or equal to (e.g., '>=5' checks if value is greater than or equal to 5)
                         - '<=': Less than or equal to (e.g., '<=10' checks if value is less than or equal to 10)

    Returns:
        bool: True if the value satisfies the condition, False otherwise.
    """
    if isblank(value):
        return False
    
    # Check if condition starts with '=' and compare value for equality
    if condition.startswith('='):
        return value == int(condition[1:])
    
    # Check if condition starts with 'in' and test if value is in the specified list
    elif condition.startswith('in'):
        try:
            values = list(map(int, condition[2:].strip()[1:-1].split(',')))
            return value in values
        except ValueError:
            return False
    
    elif condition.startswith('in '):
        try:
            values = list(map(int, condition[3:].strip()[1:-1].split(',')))
            return value in values
        except ValueError:
            return False

    # Check if condition is a 'range' and test if value falls within the range
    elif condition.startswith('range'):
        try:
            min_val, max_val = map(int, condition[5:].strip()[1:-1].split(','))
            return min_val <= value <= max_val
        except ValueError:
            return False
    
    # Check if condition starts with '>' and test if value is greater than the specified value
    elif condition.startswith('>'):
        return value > int(condition[1:])
    
    # Check if condition starts with '<' and test if value is less than the specified value
    elif condition.startswith('<'):
        return value < int(condition[1:])
    
    # Check if condition starts with '>=' and test if value is greater than or equal to the specified value
    elif condition.startswith('>='):
        return value >= int(condition[2:])
    
    # Check if condition starts with '<=' and test if value is less than or equal to the specified value
    elif condition.startswith('<='):
        return value <= int(condition[2:])
    
    # Return False for unsupported conditions
    return False
