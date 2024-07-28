from logs import Error, ErrorLog

def adderror(record, column, value=None, err_reason=None):
    err = Error(record, column, str(value), str(err_reason))
    ErrorLog.append(err)