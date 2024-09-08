from typing import Any, List, Optional
import pandas as pd
from validator_functions import *
from survey_model import *
from logs import ErrorLog, adderror

class QuestionTypes:
    def __init__(self):
        self.SINGLE         = 'single'
        self.MULTI          = 'multiple'
        self.NUMERIC        = 'number'
        self.TEXT           = 'text'
        self.NONE           = 'none'             
QUESTIONTYPES = QuestionTypes()

class Question:
    def __init__(self,id, type, parent_record,datacols=[],oecols=[]):
        self.id:str = id
        self.type:str = type
        self.datacols:List[str] = datacols
        self.oecols:List[str] = oecols
        self.parent_record = parent_record

    def is_first_record(self) -> bool:
        """
        Check if the current datarow is the first record in the dataset.
        This assumes `parent_record.row` contains row data and `parent_record` has an index or a reference to the entire dataset.
        """
        if hasattr(self.parent_record, 'index'):
            return self.parent_record.index == 0  # Assumes `index` starts at 0 for the first record
        elif hasattr(self.parent_record, 'row_number'):
            return self.parent_record.row_number == 1  # Assumes `row_number` is 1-based

        return False

    def validate(self,qtype=QUESTIONTYPES.SINGLE,valid_values: list = [0,1], optional_cols: list = [], exclude_cols: list = [], exclusive_cols: list = [],range_param=(0,100),at_least: int = 1, at_most: int = -1, txt_mnlen=1,txt_mxlen:Any=None,allowblanks: bool = False, required: int = 1, condition: bool = True):
        datarow = self.parent_record.row

        if self.is_first_record():
            if qtype != self.type:
                adderror(0,self.id,0,"Question type mismatch.")

        if qtype==QUESTIONTYPES.SINGLE:
            self.validatesingle(valid_values,optional_cols,exclude_cols,allowblanks,condition)

        if qtype==QUESTIONTYPES.MULTI:
            self.validatemulti(valid_values,optional_cols,exclude_cols,exclusive_cols,at_least,at_most,allowblanks,required,condition)

        if qtype==QUESTIONTYPES.NUMERIC:
            self.validatenumeric(optional_cols,exclude_cols,exclusive_cols,range_param,at_least,at_most,allowblanks,required,condition)

        if qtype==QUESTIONTYPES.TEXT:
            self.validatesingle(optional_cols,exclude_cols,exclusive_cols,at_least,at_most,txt_mnlen,txt_mxlen,allowblanks,required,condition) # type: ignore

    def validatesingle(self,valid_values, optional_cols: list = [], exclude_cols: list = [], allowblanks: bool = False, required: int = 1, condition: bool = True):
        datarow = self.parent_record.row
        validatesingle(self.id,self.datacols,datarow,valid_values,optional_cols,exclude_cols,allowblanks,condition)


    def validatemulti(self,valid_values: list = [0,1], optional_cols: list = [], exclude_cols: list = [], exclusive_cols: list = [],at_least: int = 1, at_most: int = -1, allowblanks: bool = False, required: int = 1, condition: bool = True):
        datarow = self.parent_record.row
        validatemulti(self.id,self.datacols,datarow,valid_values,optional_cols,exclude_cols,exclusive_cols,
                      at_least,at_most,allowblanks,required,condition)

    def validatenumeric(self, optional_cols: list = [], exclude_cols: list = [], exclusive_cols: list = [],range_param=(0,100),at_least: int = 1, at_most: int = -1, allowblanks: bool = False, required: int = 1, condition: bool = True):
        datarow = self.parent_record.row
        validatenumeric(self.id,self.datacols,datarow,optional_cols,exclude_cols,exclusive_cols,
                      at_least,at_most,allowblanks,required,condition,range_param)

    def validatetext(self,optional_cols: list = [], exclude_cols: list = [], exclusive_cols: list = [],at_least: int = 1, at_most: int = -1, txt_mnlen=1,txt_mxlen:Any=None,allowblanks: bool = False, required: int = 1, condition: bool = True):
        datarow = self.parent_record.row
        validatetext(self,self.datacols,datarow,optional_cols,exclude_cols,exclusive_cols,
                     at_least,at_most,txt_mnlen,txt_mxlen,allowblanks,required,condition)

    def checksum(self,exclude_cols: list = [], condition: bool = True, sum_condition: str = '=100'):
        datarow = self.parent_record.row
        checksum(self.id,self.datacols,datarow,exclude_cols,condition,sum_condition)

    def checksum100(self,exclude_cols: list = [], condition: bool = True):
        datarow = self.parent_record.row
        checksum100(self.id,self.datacols,datarow,exclude_cols,condition)

    def checkrank(self,min_rank_value: int = 1, max_rank_value: Optional[int] = None, exclude_cols: list = [], condition: bool = True):
        datarow = self.parent_record.row
        checkrank(self.id,self.datacols,datarow,min_rank_value,max_rank_value,exclude_cols,condition)

    def checkblanks(self, exclude_cols: list = [], condition: bool = True):
        datarow = self.parent_record.row
        checkblanks(self.id,self.datacols,datarow,exclude_cols,condition)

    def checknonblanks(self, exclude_cols: list = [], condition: bool = True):
        datarow = self.parent_record.row
        checknonblanks(self.id,self.datacols,datarow,exclude_cols,condition)