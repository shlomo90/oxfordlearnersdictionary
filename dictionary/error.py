from enum import Enum


ERRNUM = Enum("OK", "E_ARGS", "E_NODICT")
ERRMSG = {
    ERRNUM.OK: "OK",
    ERRNUM.E_ARGS: "Need Argument at least one",
    ERRNUM.E_NODICT: "No Dictionary",}


class DictionaryError(Exception):
    pass


def print_error_msg(error_code):
    print("{}".format(ERRMSG[error_code]))
