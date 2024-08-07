from survey_model import DATA, COLUMNS, QUESTIONS, Column, Columns, Question, Questions 
import pandas as pd
import numpy as np
import re
from typing import List
from logs import Error, ErrorLog,adderror
import pandas as pd
from .CheckMasking import CheckMasking

def checkQuestionMasking(question: Question, mask_question: Question, condition: str, always_showcols: List[str]):
    CheckMasking(question.datacols, mask_question.datacols, condition, always_showcols)