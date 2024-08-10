from decorative_logging import log_memory_usage, log_profiling_data, log_execution, log_execution_time

# @log_exceptions(exit_on_catch=True)
@log_execution("warning", 'log.txt')
@log_execution_time("info")
@log_memory_usage("info")
@log_profiling_data("info")
def add(num1, num2):
    return num1 + num2

add(1,2)