from decorative_logging import utils
import sys
import functools
from time import perf_counter
import cProfile
import pstats
from io import StringIO
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.padding import Padding


def log_execution(level="debug", filename=None):
    """
    Logs the execution of the decorated function

    Log format
    ----------
        [LEVEL] <Date> <Time> - log_excecution:<func_name>\n
        \--------------------------------------------------\n
        FUNCTION CALL: func_name(args, kwargs)
        RETURNED VALUE: <function return val>

    Parameters
    ----------
    level : str, default 'debug'
        Log level, one of ['debug', 'info', 'warning', 'error', 'critical']
    filename : str, default None
        Name of file to which to write execution logs for the decorated function
    """
    level = utils.clean_and_check_level(level)

    def execution_logger(func):
        logger, log_func = utils.get_logger(
            f"log_execution:{func.__name__}", level, filename
            )

        @functools.wraps(func)
        def log(*args, **kwargs):
            # print(func_args)
            result = func(*args, **kwargs)
            log_msg = "FUNCTION CALL: "
            log_msg += func.__name__
            log_msg += utils.get_arg_string(*args, **kwargs) + "\n"
            log_msg += "RETURNED VALUE: " + str(utils.clean_result(result))

            log_func(log_msg)
            return result

        return log
    return execution_logger


def log_exceptions(exit_on_catch=True, level="error", filename=None):
    """
    Logs any exceptions thrown during execution of the decorated function

    Log format
    ----------
        [LEVEL] <Date> <Time> - log_exceptions:<func_name>\n
        \--------------------------------------------------\n
        Exception thrown from call to func_name(args, kwargs):\n
        ErrorType('Error Message')\n
        exit_on_catch == False, ignoring and returning None

    Parameters
    ----------
    exit_on_catch : bool, default True
        Determines if the program halts when an exception is caught or if it
        returns None from the wrapped function and continues
    level : str, default 'debug'
        Log level, one of ['debug', 'info', 'warning', 'error', 'critical']
    filename : str, default None
        Name of file to which to write exception logs for the decorated function
    """
    level = utils.clean_and_check_level(level)

    def inner(func):
        logger, log_func = utils.get_logger(
            f"log_exceptions:{func.__name__}", level, filename
            )

        @functools.wraps(func)
        def log(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_msg = "Exception thrown from call to " + func.__name__
                log_msg += utils.get_arg_string(*args, **kwargs) + ":\n"
                if filename is not None:
                    log_msg += repr(e) + '\n'
                else:
                    log_msg += "\x1b[31;20m" + repr(e) + "\033[0m\n"
                log_msg += "exit_on_catch == " + str(exit_on_catch) + ", "
                if exit_on_catch:
                    log_msg += "exiting with code 1...\n"
                    log_func(log_msg)
                    sys.exit(1)
                log_msg += "ignoring and returning None\n"
                log_func(log_msg)
                return None
        return log
    return inner


def log_execution_time(level="debug", filename=None):
    """
    Logs the execution time of the decorated function

    Log format
    ----------
        [LEVEL] <Date> <Time> - log_execution_time:<func_name>\n
        \--------------------------------------------------\n
        Run-time for execution of func_name(args=(), kwargs={}): X.XXXXX seconds

    Parameters
    ----------
    level : str, default 'debug'
        Log level, one of ['debug', 'info', 'warning', 'error', 'critical']
    filename : str, default None
        Name of file to which to write execution time logs for the decorated function
    """
    level = utils.clean_and_check_level(level)

    def time_logger(func):
        logger, log_func = utils.get_logger(
            f"log_execution_time:{func.__name__}", level, filename
            )

        @functools.wraps(func)
        def timer(*args, **kwargs):
            start_time = perf_counter()
            ret = func(*args, **kwargs)
            end_time = perf_counter()
            delta = end_time - start_time
            log_msg = "Run-time for execution of " + func.__name__
            log_msg += utils.get_arg_string(*args, **kwargs) + ": "
            log_msg += str(delta) + " seconds\n"
            log_func(log_msg)
            return ret
        return timer
    return time_logger


def custom_logger(name, message, level, filename=None):
    """
    Logs the execution of the decorated function

    Logs function calls at the specified log level with the format
        FUNCTION CALL: func_name(args, kwargs)
        RETURNED VALUE: <function return val>

    Parameters
    ----------
    level : str, default 'debug'
        Log level, one of ['debug', 'info', 'warning', 'error', 'critical']
    filename : str, default None
        Name of file to which to write the custom logs for the decorated function
    """
    level = utils.clean_and_check_level(level)
    logger, log_func = utils.get_logger(name, level, filename)

    def log_custom(func):
        log_func(message)

        @functools.wraps(func)
        def return_func(*args, **kwargs):
            return func(*args, **kwargs)

        return return_func
    return log_custom


def log_memory_usage(level="debug", filename=None):
    """
    Logs the memory usage of the decorated function

    Log format
    ----------
        [LEVEL] <Date> <Time> - log_memory_usage:<func_name>\n
        \--------------------------------------------------\n
        Memory usage for execution of func_name(args=(), kwargs={}):\n
        Peak memory usage during execution: XX.XXXX MB | Change from before execution: XX.XXXX KB

    Parameters
    ----------
    level : str, default 'debug'
        Log level, one of ['debug', 'info', 'warning', 'error', 'critical']
    filename : str, default None
        Name of file to which to write memory logs for the decorated function
    """
    level = utils.clean_and_check_level(level)

    def memory_logger(func):
        logger, log_func = utils.get_logger(
            f"log_memory_usage:{func.__name__}", level, filename
            )

        @functools.wraps(func)
        def log(*args, **kwargs):
            mem_before = utils.get_process_memory()
            result = func(*args, **kwargs)
            mem_after = utils.get_process_memory()
            log_msg = "Memory usage for execution of " + func.__name__
            log_msg += utils.get_arg_string(*args, **kwargs) + ":\n"
            log_msg += "Peak memory usage during execution: "
            log_msg += utils.format_mem_size(mem_after)
            log_msg += " | Change from before execution: "
            log_msg += utils.format_mem_size(mem_after - mem_before) + "\n"
            log_func(log_msg)
            return result

        return log
    return memory_logger

def log_profiling_data(level="debug", stats_order='cumtime', filename=None):
    """
    Logs the execution of the decorated function

    Logs function calls at the specified log level with the format
        FUNCTION CALL: func_name(args, kwargs)
        RETURNED VALUE: <function return val>

    Parameters
    ----------
    level : str, default 'debug'
        Log level, one of ['debug', 'info', 'warning', 'error', 'critical']
    filename : str, default None
        Name of file to which to write profiling logs for the decorated function
    """
    level = utils.clean_and_check_level(level)

    def cpu_logger(func):
        logger, log_func = utils.get_logger(
            f"log_profiling_data:{func.__name__}", level, filename
            )

        @functools.wraps(func)
        def log(*args, **kwargs):
            with cProfile.Profile() as pr:
                pr.enable()
                result = func(*args, **kwargs)
                pr.create_stats()
                string_stream = StringIO()
                ps = pstats.Stats(pr, stream=string_stream)
                ps.sort_stats(stats_order)
                ps.print_stats()
                panel_title = "Profiling Data for " + func.__name__
                panel_title += utils.get_arg_string(*args, **kwargs)
                stats = string_stream.getvalue()
                stats_lines = [i.strip() for i in stats.split("\n") if i != '']
                stats_dict = {
                    "calls_summary": Padding(stats_lines[0], (1)),
                    "list_order": stats_lines[1],
                    "col_headers": stats_lines[2].split(),
                    "data_rows": [" ".join(
                                    line.split()
                                  ).split(' ', 5) for line in stats_lines[3:]]
                }
                table = Table(
                    title=stats_dict['calls_summary'],
                    show_lines=True
                )
                for header in stats_dict['col_headers']:
                    table.add_column(header, justify="center")
                for row in stats_dict['data_rows']:
                    table.add_row(*row)
                console = Console(file=StringIO())
                console.print(
                    Panel(
                        table,
                        title=panel_title,
                        subtitle=stats_dict['list_order']
                    )
                )
                str_output = console.file.getvalue()
                log_func(str_output)
                return result

        return log
    return cpu_logger
