import time
from functools import wraps

def timed_log(logger):
    """This decorator prints the execution time for the decorated function."""
    def inner_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logger.debug("{} ran in {}s".format(func.__name__, round(end - start, 3)))
            return result
        return wrapper
    return inner_wrapper
