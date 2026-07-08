import logging
import sys


def error_message_detail(error: Exception, error_detail) -> str:
    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is None:
        return f"Error message [{str(error)}]"

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = (
        "Error occurred in python script name [{0}] "
        "line number [{1}] "
        "error message [{2}]"
    ).format(file_name, exc_tb.tb_lineno, str(error))

    return error_message


class CustomException(Exception):
    def __init__(self, error: Exception, error_detail):
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_detail)

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        logging.info("Divide by zero error")
        raise CustomException(e, sys) from None
