from typing import List
import pandas as pd

from logs import *

def geterrors():
    for error in ErrorLog:
        print(error.record,error.err_reason,error.errorcolumn,error.errorvalue)
