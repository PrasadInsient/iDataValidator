from typing import List
import pandas as pd

class Question:
    def __init__(self,id, type, text, rows=[],cols=[],datacols=[],oecols=[],data=pd.DataFrame()):
        self.id:str = id
        self.type:str = type
        self.text:str = text
        self.rows:List[str] = rows
        self.cols:List[str] = cols
        self.datacols:List[str] = datacols
        self.oecols:List[str] = oecols
        self.surveydata:pd.DataFrame = data

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'text': self.text,
            'rwos': self.rows
        }
