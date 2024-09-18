import logging
# import inspect
import os
import psutil


class CustomFormatter(logging.Formatter):

    green = "\033[92m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\033[0m"
    level = "%(levelname)s"
    format = f'%(asctime)s - %(name)s\n{"-"*50}\n%(message)s\n'

    FORMATS = {
        logging.DEBUG: "[" + green + level + reset + "] " + format + reset,
        logging.INFO: "[" + green + level + reset + "] " + format + reset,
        logging.WARNING: "[" + yellow + level + reset + "] " + format + reset,
        logging.ERROR: "[" + red + level + reset + "] " + format + reset,
        logging.CRITICAL: bold_red + "[" + level + "] " + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class CustomFileFormatter(logging.Formatter):

    green = "\033[92m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\033[0m"
    level = "%(levelname)s"
    format = f'%(asctime)s - %(name)s\n{"-"*50}\n%(message)s\n'

    FORMATS = {
        logging.DEBUG: "[" + level + "] " + format,
        logging.INFO: "[" + level + "] " + format,
        logging.WARNING: "[" + level + "] " + format,
        logging.ERROR: "[" + level + "] " + format,
        logging.CRITICAL: "[" + level + "] " + format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def get_arg_string(*args, **kwargs):
    arg_str = "(args=" + str(args) + ", kwargs=" + str(kwargs) + ")"
    return arg_str


def string_to_level(level_string):
    if level_string == 'debug':
        return logging.DEBUG
    if level_string == 'info':
        return logging.INFO
    if level_string == 'warning':
        return logging.WARNING
    if level_string == 'error':
        return logging.ERROR
    if level_string == 'critical':
        return logging.CRITICAL


def string_to_log_func(logger, level_string):
    if level_string == 'debug':
        return logger.debug
    if level_string == 'info':
        return logger.info
    if level_string == 'warning':
        return logger.warning
    if level_string == 'error':
        return logger.error
    if level_string == 'critical':
        return logger.critical


def get_stream_handler(base_level='debug', formatter=CustomFormatter):
    formatted_stream_handler = logging.StreamHandler()
    formatted_stream_handler.setLevel(string_to_level(base_level))
    # add formatter to formatted_stream_handler
    formatted_stream_handler.setFormatter(CustomFormatter())
    return formatted_stream_handler


def get_file_handler(filename, base_level='debug', formatter=CustomFileFormatter):
    formatted_file_handler = logging.FileHandler(filename)
    formatted_file_handler.setLevel(string_to_level(base_level))
    formatted_file_handler.setFormatter(CustomFileFormatter())
    return formatted_file_handler


def get_logger(name, level, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(string_to_level(level))
    logger.addHandler(get_stream_handler(level))
    if filename is not None:
        logger.addHandler(get_file_handler(filename, level))
    log_func = string_to_log_func(logger, level)
    return logger, log_func


def clean_result(result, show_length = 50):
    res_str = str(result)
    if len(res_str) > 100:
        res_str = ''.join(res_str[:show_length]) + " ... " + ''.join(res_str[-show_length:])
    return res_str


def get_process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def format_mem_size(bytes):
    if bytes > 500000000:
        ret_float, suffix = (bytes/1000.0/1000.0/1000.0, " GB")
    elif bytes > 10000000:
        ret_float, suffix = (bytes/1000.0/1000.0, " MB")
    else:
        ret_float, suffix = (bytes/1000.0, " KB")
    ret_float = format(ret_float, '.4f')
    return str(ret_float) + suffix


def clean_and_check_level(level_arg):
    level_arg = level_arg.lower()
    if level_arg in ['debug', 'info', 'warning', 'error', 'critical']:
        return level_arg
    raise ValueError(
        ' '.join(["Invalid log level provided, must be one of",
                  "['debug', 'info', 'warning', 'error', 'critical']"])
        )
