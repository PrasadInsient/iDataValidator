from typing import Any
from logs import Error, ErrorLog

def adderror(record:Any, column:Any, value:Any=None, err_reason:str=""):
    err = Error(record, column, str(value), str(err_reason))
    ErrorLog.append(err)