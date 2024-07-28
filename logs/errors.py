from typing import List
import pandas as pd

class Error:
    def __init__(self, record, column, value="", err_reason=""):
        self.record: str = str(record)
        self.errorcolumn: str = str(column)
        self.errorvalue: str = str(value)
        self.err_reason: str = str(err_reason)

ErrorLog: List[Error] = []
