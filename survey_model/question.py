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

    def validate(self,qtype=QUESTIONTYPES.SINGLE,valid_values = [0,1], optional_cols: list = [],  exclusive_cols: list = [],
                 ignore_cols: list = [],range_param=(0,100),at_least: int = 1, at_most: int = -1, txt_mnlen=1,txt_mxlen:Any=None,
                 allowblanks: bool = False, required: int = 1, condition: bool = True):

        if qtype==QUESTIONTYPES.SINGLE:
            self.validatesingle(valid_values,optional_cols,ignore_cols,allowblanks,condition)

        if qtype==QUESTIONTYPES.MULTI:
            self.validatemulti(valid_values,optional_cols,exclusive_cols,ignore_cols,at_least,at_most,allowblanks,required,condition)

        if qtype==QUESTIONTYPES.NUMERIC:
            self.validatenumeric(optional_cols,exclusive_cols,ignore_cols,range_param,at_least,at_most,allowblanks,required,condition)

        if qtype==QUESTIONTYPES.TEXT:
            self.validatesingle(optional_cols,exclusive_cols,ignore_cols,at_least,at_most,txt_mnlen,txt_mxlen,allowblanks,required,condition) # type: ignore


    def validatesingle(self,valid_values, optional_cols: list = [], ignore_cols: list = [], allowblanks: bool = False, required: int = 1, condition: bool = True):

        datarow = self.parent_record.row
        validatesingle(self.id,self.datacols,datarow,valid_values,optional_cols,ignore_cols,allowblanks,condition)


    def validatemulti(self,valid_values: list = [0,1], optional_cols: list = [], exclusive_cols: list = [],ignore_cols: list = [],at_least: int = 1, at_most: int = -1, allowblanks: bool = False, required: int = 1, condition: bool = True):

        datarow = self.parent_record.row
        validatemulti(self.id,self.datacols,datarow,valid_values,optional_cols,exclusive_cols,ignore_cols,
                      at_least,at_most,allowblanks,required,condition)

    def validatenumeric(self, optional_cols: list = [], exclusive_cols: list = [],ignore_cols: list = [],range_param=(0,100),at_least: int = 1, at_most: int = -1, allowblanks: bool = False, required: int = 1, condition: bool = True):
        datarow = self.parent_record.row
        validatenumeric(self.id,self.datacols,datarow,optional_cols,exclusive_cols,ignore_cols,
                      at_least,at_most,allowblanks,required,condition,range_param)

    def validatetext(self,optional_cols: list = [],  exclusive_cols: list = [],ignore_cols: list = [],at_least: int = 1, at_most: int = -1, txt_mnlen=1,txt_mxlen:Any=None,allowblanks: bool = False, required: int = 1, condition: bool = True):
        datarow = self.parent_record.row
        validatetext(self,self.datacols,datarow,optional_cols,exclusive_cols,ignore_cols,
                     at_least,at_most,txt_mnlen,txt_mxlen,allowblanks,required,condition)

    def checksum(self,ignore_cols: list = [], sum_condition: str = '=100', condition: bool = True):
        datarow = self.parent_record.row
        checksum(self.id,self.datacols,datarow,sum_condition,ignore_cols,condition)

    def checksum100(self,ignore_cols: list = [], sum_condition: str = '=100',condition: bool = True):
        datarow = self.parent_record.row
        checksum100(self.id,self.datacols,datarow,sum_condition,ignore_cols,condition)

    def checkrank(self,min_rank_value: int = 1, max_rank_value: Optional[int] = None, ignore_cols: list = [], condition: bool = True):
        datarow = self.parent_record.row
        checkrank(self.id,self.datacols,datarow,min_rank_value,max_rank_value,ignore_cols,condition)

    def checkblanks(self, ignore_cols: list = [], condition: bool = True):
        datarow = self.parent_record.row
        checkblanks(self.id,self.datacols,datarow,ignore_cols,condition)

    def checknonblanks(self, ignore_cols: list = [], condition: bool = True):
        datarow = self.parent_record.row
        checknonblanks(self.id,self.datacols,datarow,ignore_cols,condition)


    def checkexclusive(self, questionid: str, datacols: list, exclusive_cols: list = [], 
                   iszerovalid: bool = True, condition: bool = True, oneway: bool = False):
        datarow = self.parent_record.row
        checkexclusive(questionid, datacols, datarow, exclusive_cols,iszerovalid, condition, oneway)

    def checkmasking(self,maskcond_cols: List[str],maskcondition: str ="=1",  always_showcols: List[str]=[], condition= True):
        datarow = self.parent_record.row
        checkmasking(self.id, datarow, self.datacols,maskcond_cols,maskcondition,always_showcols,condition)

    def backchecksingle(self,cols_to_check: List[str],backcheckcondition: str, condition: bool = True):
        datarow = self.parent_record.row
        backchecksingle(self.id, datarow,self.datacols[0],cols_to_check, backcheckcondition, condition)

    def backcheckmulti(self,cols_to_check: List[str],backcheckcondition: str ="=1",  
        always_showcols: List[str]=[],ignoresourcecols:List[str]=[],ignoretargetcols:List[str]=[],condition= True):
        datarow = self.parent_record.row
        backcheckmulti(self.id,  datarow, self.datacols,cols_to_check,backcheckcondition,
                       always_showcols,ignoresourcecols,ignoretargetcols,condition)