from decorative_logging import log_execution_time, custom_logger
from time import sleep
# @log_exceptions(exit_on_catch=True)
@custom_logger("custom message: add()", "This is a custom log message", "warning")
@log_execution_time("critical")
def add(num1, num2):
    # sleep(0.5)
    return num1 + num2

add(1,2)