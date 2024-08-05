from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions
from typing import List
import pandas as pd
import numpy as np
import re
from validator_functions.question_validator_functions import *
from validator_functions.record_validator_functions import *
from .record_validator import *
from .unit_validators import *
from functools import partial
def question_validator():
  pass