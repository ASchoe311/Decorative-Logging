from decorative_logging.decorators import log_memory_usage, log_execution, log_execution_time, log_profiling_data
import random
from time import sleep

@log_execution_time("warning")
@log_memory_usage("info")
# @log_execution("debug")
@log_profiling_data("info")
def func():
    big_list = [i for i in range(1000000)]
    random.shuffle(big_list)
    big_list = sorted(big_list)
 
func()

@log_execution_time("warning")
@log_memory_usage("info")
# @log_execution("debug")
@log_profiling_data("info")
def MakeMatrix (dim):
    matrix = []   
    for i in range (dim):
        matrix.append([j for j in range (dim)])
    return (matrix)
MakeMatrix(5000)