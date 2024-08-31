DecorativeLogging is a tool to aid developers in creating their own Python applications by simplifying the process of logging various aspects of function execution. Goodbye boilerplate logging code, hello decorators!

So far the decorators available are:

* Execution logger - Logs that a decorated function has been executed including the arguments passed to it and its return value
* Exception logger - Logs any execptions thrown during the execution of a decorated function
* Execution time logger - Logs the execution time of a decorated function
* Memory usage logger - Logs the memory used by a decorated function
* CPU profiling logger - Logs a table containing profiling information from cProfile for a decorated function

These decorators can be chained* to log all the information you could want about a function, and can be directed to log with different log levels and either to standard output or directly to a file.

*CPU profiling logger cannot be chained unless it is the last logger in the chain so as to prevent it from profiling the other decorators.


# Installation

    Not yet available on PyPi! For now install from source
	
### Requirements

 - [rich](https://github.com/Textualize/rich)

# Usage example
## Logs the running of a simple function that creates a big list, shuffles it, then sorts it
	import decorative_logging.decorators as deco
    import random


    @deco.log_memory_usage("info")
    @deco.log_execution_time("warning")
    @deco.log_execution("debug")
    @deco.log_profiling_data("info", filename="log.txt")
    def shuffle_and_sort_list(listsize):
        big_list = [i for i in range(listsize)]
        random.shuffle(big_list)
        big_list = sorted(big_list)
    
    shuffle_and_sort_list(1000000)

## This example program would produce the following output
![Sample code output](https://i.imgur.com/IRNajei.png)