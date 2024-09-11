from typing import List, Optional, Any
import pandas as pd
from validator_functions import *  # Assuming validation functions are imported here


class QuestionTypes:
    """
    A class to define the types of questions handled by the DataRecordBase class.
    """
    def __init__(self):
        self.SINGLE = 'single'
        self.MULTI = 'multiple'
        self.NUMERIC = 'number'
        self.TEXT = 'text'
        self.NONE = 'none'


# Global constant for question types
QUESTIONTYPES = QuestionTypes()


class DataRecordBase:
    """
    Base class for data records, providing various validation methods for different types of questions.
    This class expects each instance to have access to `self.row`, which represents a row of data to be validated.
    """
    
    def __init__(self):
        pass
    
    def validate(
        self, 
        questionid, 
        qtype=QUESTIONTYPES.SINGLE, 
        valid_values = [0, 1], 
        datacols: List[str] = [], 
        optional_cols: List[str] = [], 
        exclusive_cols: List[str] = [], 
        ignore_cols: List[str] = [], 
        range_param=(0, 100), 
        at_least: int = 1, 
        at_most: int = -1, 
        txt_mnlen: int = 1, 
        txt_mxlen: Optional[int] = None, 
        allowblanks: bool = False, 
        required: int = 1, 
        condition: bool = True
    ):
        """
        General validation method that calls specific validation functions based on question type.

        Parameters:
        -----------
        questionid : str
            The unique identifier for the question being validated.

        qtype : str, optional
            Type of question (e.g., 'single', 'multiple', 'number'), by default 'single'.

        valid_values : List[int], optional
            List of valid values for 'single' and 'multiple' question types, by default [0, 1].

        datacols : List[str], optional
            List of column names to validate, by default an empty list.

        optional_cols : List[str], optional
            List of columns that are optional for validation, by default an empty list.

        ignore_cols : List[str], optional
            List of columns to exclude from validation, by default an empty list.

        exclusive_cols : List[str], optional
            List of columns for exclusive validation (used for 'multiple' question type), by default an empty list.

        range_param : tuple, optional
            A tuple representing the minimum and maximum values for numeric validation, by default (0, 100).

        at_least : int, optional
            Minimum number of selections required for 'multiple' questions, by default 1.

        at_most : int, optional
            Maximum number of selections allowed for 'multiple' questions, by default -1 (no limit).

        txt_mnlen : int, optional
            Minimum length for text validation, by default 1.

        txt_mxlen : int, optional
            Maximum length for text validation, by default None.

        allowblanks : bool, optional
            Whether blanks are allowed in validation, by default False.

        required : int, optional
            Whether the question is required (1 for required, 0 for optional), by default 1.

        condition : bool, optional
            Additional condition to enable validation, by default True.
        """

        if qtype == QUESTIONTYPES.SINGLE:
            self.validatesingle(questionid, datacols, valid_values, optional_cols, ignore_cols, allowblanks, condition)

        if qtype == QUESTIONTYPES.MULTI:
            self.validatemulti(questionid, datacols, valid_values, optional_cols, exclusive_cols, ignore_cols, at_least, at_most, allowblanks, required, condition)

        if qtype == QUESTIONTYPES.NUMERIC:
            self.validatenumeric(questionid, datacols, optional_cols, exclusive_cols, ignore_cols, range_param, at_least, at_most, allowblanks, required, condition)

        if qtype == QUESTIONTYPES.TEXT:
            self.validatetext(questionid, datacols, optional_cols, exclusive_cols, ignore_cols, at_least, at_most, txt_mnlen, txt_mxlen, allowblanks, required, condition)

    def validatesingle(self, questionid, datacols, valid_values, optional_cols=[], ignore_cols=[], allowblanks=False, condition=True):
        """
        Validate single-choice questions.
        """
        datarow = self.row #type:ignore
        validatesingle(questionid, datacols, datarow, valid_values, optional_cols, ignore_cols, allowblanks, condition)

    def validatemulti(self, questionid, datacols, valid_values=[0, 1], optional_cols=[], exclusive_cols=[], ignore_cols=[], at_least=1, at_most=-1, allowblanks=False, required=1, condition=True):
        """
        Validate multi-choice questions with possible exclusivity and at_least/at_most constraints.
        """
        datarow = self.row #type:ignore
        validatemulti(questionid, datacols, datarow, valid_values, optional_cols, exclusive_cols, ignore_cols, at_least, at_most, allowblanks, required, condition)

    def validatenumeric(self, questionid, datacols, optional_cols=[], exclusive_cols=[], ignore_cols=[], range_param=(0, 100), at_least=1, at_most=-1, allowblanks=False, required=1, condition=True):
        """
        Validate numeric questions, ensuring values fall within the specified range.
        """
        datarow = self.row #type:ignore
        validatenumeric(questionid, datacols, datarow, optional_cols, exclusive_cols, ignore_cols, at_least, at_most, allowblanks, required, condition, range_param)

    def validatetext(self, questionid, datacols, optional_cols=[], exclusive_cols=[], ignore_cols=[], at_least=1, at_most=-1, txt_mnlen=1, txt_mxlen=None, allowblanks=False, required=1, condition=True):
        """
        Validate text questions by ensuring the text length falls within the allowed range.
        """
        datarow = self.row #type:ignore
        validatetext(questionid, datacols, datarow, optional_cols, exclusive_cols, ignore_cols, at_least, at_most, txt_mnlen, txt_mxlen, allowblanks, required, condition)

    def checksum(self, questionid, datacols, sum_condition='=100', ignore_cols=[], condition=True):
        """
        Validate that the sum of selected values across multiple columns satisfies the given condition.
        """
        datarow = self.row #type:ignore
        checksum(questionid, datacols, datarow,  sum_condition, ignore_cols,condition)

    def checksum100(self, questionid, datacols, ignore_cols=[], condition=True):
        """
        Validate that the sum of values across multiple columns equals 100.
        """
        datarow = self.row #type:ignore
        checksum100(questionid, datacols, datarow, '=100', ignore_cols, condition)

    def checkrank(self, questionid, datacols, min_rank_value=1, max_rank_value=None, ignore_cols=[], condition=True):
        """
        Validate ranking questions, ensuring the ranking falls between specified minimum and maximum values.
        """
        datarow = self.row #type:ignore
        checkrank(questionid, datacols, datarow, min_rank_value, max_rank_value, ignore_cols, condition)

    def checkblanks(self, questionid, datacols, ignore_cols=[], condition=True):
        """
        Validate that no blanks exist in the specified columns.
        """
        datarow = self.row #type:ignore
        checkblanks(questionid, datacols, datarow, ignore_cols, condition)

    def checknonblanks(self, questionid, datacols, ignore_cols=[], condition=True):
        """
        Validate that all required columns contain non-blank values.
        """
        datarow = self.row #type:ignore
        checknonblanks(questionid, datacols, datarow, ignore_cols, condition)

    def checkexclusive(self, questionid: str, datacols: list, exclusive_cols: list = [], 
                   iszerovalid: bool = True, condition: bool = True, oneway: bool = False):
        datarow = self.row #type:ignore
        checkexclusive(questionid, datacols, datarow, exclusive_cols,iszerovalid, condition, oneway)

    def checkmasking(self,questionid,question_cols: List[str], maskcond_cols: List[str], 
                 maskcondition: str ="=1",  always_showcols: List[str]=[], condition= True):
        datarow = self.row #type:ignore
        checkmasking(questionid, datarow, question_cols,maskcond_cols,maskcondition,always_showcols,condition)

    def backchecksingle(self,questionid: str, qcol: str, cols_to_check: List[str], 
                     backcheckcondition: str, condition: bool = True):
        datarow = self.row #type:ignore
        backchecksingle(questionid, datarow,qcol,cols_to_check, backcheckcondition, condition)

    def backcheckmulti(self,questionid: str, question_cols: List[str],  cols_to_check: List[str],backcheckcondition: str ="=1",  
        always_showcols: List[str]=[],ignoresourcecols:List[str]=[],ignoretargetcols:List[str]=[],condition= True):
        datarow = self.row #type:ignore
        backcheckmulti(questionid,  datarow, question_cols,cols_to_check,backcheckcondition,
                       always_showcols,ignoresourcecols,ignoretargetcols,condition)

    def checktwowayGG(self,GGquestion: str, GGprices=[], priceq: str = "",
                  start_pos=3, no_times=3, hideinvalidoptions=1, order=1, condition: bool = True):
        datarow = self.row #type:ignore
        checktwowayGG(GGquestion,datarow,GGprices,priceq,start_pos,no_times,hideinvalidoptions,order,condition)

    def checkonewayGG(self,GGquestion: str, GGprices=[], priceq: str = "",
                  start_pos=3, no_times=3, hideinvalidoptions=1, order=1, condition: bool = True):
        datarow = self.row #type:ignore
        checkonewayGG(GGquestion,datarow,GGprices,priceq,start_pos,no_times,hideinvalidoptions,order,condition)