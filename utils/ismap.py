from dataclasses import dataclass
from typing import Any, Dict, List

class QuestionTypes:
    def __init__(self):
        self.SINGLE         = 'single'
        self.MULTI          = 'multiple'
        self.NUMERIC        = 'number'
        self.TEXT           = 'text'
        self.NONE           = 'none'   

def IS_GetQuestions()->List[Dict[str, str]]:
    questionsMap = []
    questionObj = {}
    questionObj['qlabel']="Q1"
    questionObj['qtype'] = "single"
    questionObj['qdataColumnsNames']=["Q1"]
    questionObj['qOEColumnsNames']=[]
    questionsMap.append(questionObj)
    return questionsMap


def IS_GetColumns()->List[Dict[str, str]]:
    columnsMap = []
    columnObj = {}
    columnObj['type'] = "single"
    columnObj['label'] = "Q1"
    columnsMap.append(columnObj)
    return columnsMap

