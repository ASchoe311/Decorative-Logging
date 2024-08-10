from decorative_logging.decorators import log_exceptions, log_execution, log_execution_time

def throw_exception():
    raise ValueError('A very specific bad thing happened.')

def do_nothing():
    pass

@log_exceptions(exit_on_catch=False, filename='log.txt')
@log_execution("debug")
def bad_call_go(*args, **kwargs):
    throw_exception()

@log_exceptions(exit_on_catch=True, filename='log.txt')
@log_execution("debug")
def bad_call_stop(*args, **kwargs):
    throw_exception()

@log_execution_time('debug')
@log_exceptions(exit_on_catch=False, filename='log.txt')
@log_execution("debug")
def good_call(*args, **kwargs):
    do_nothing()

bad_call_go(1, g=5)
good_call(3, a=2)
bad_call_stop()
good_call()