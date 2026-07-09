import sys 
from src.logger import logging

class CustomException(Exception):
    def __init__(self, error_message,error_detail:sys):
        self.error_message = error_message
        exc_type,exc_value,exc_traceback = error_detail.exc_info()
        self.lineno = exc_traceback.tb_lineno
        self.file_name = exc_traceback.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python scrip of name {self.file_name}, line number {self.lineno}, error message is {str(self.error_message)}"
    

if __name__ == "__main__":
    try:
        logging.info("Exception handling check")
        a=1/0
        print("This will not be printed")
    except Exception as e:
        raise CustomException(e,sys)
