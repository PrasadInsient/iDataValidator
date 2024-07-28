from typing import List
import pandas as pd
class Column:
    def __init__(self, label,type,data=pd.DataFrame()):
        self.label:str = label
        self.type:str = type
        self.data:pd.DataFrame = data

    def __str__(self):
        return self.label

    #def assign_data(self, data_frame):
    #    self.data = data_frame[self.label] if self.label in data_frame.columns else None

    def __repr__(self):
        return self.label

