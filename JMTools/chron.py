from time import perf_counter
from functools import wraps
from typing import Callable


def chron(f: Callable) -> Callable:
    """Wraps a function into a timeable function.

    Parameters
    ----------
    f : Callable
        Function to be timed. Add the kwarg timed=True to have it timed.

    Returns
    -------
    Callable
        Wrapped function that is timed. If timed=True, prints the name of the
        function along with execution time.
    """
    @wraps(f)  # Needed to keep f's docstring
    def timedf(*args, **kwargs):
        timed = kwargs.pop('timed', False)
        ts = perf_counter()
        result = f(*args, **kwargs)
        te = perf_counter()
        if timed:
            print(f'Function {f.__name__} took {te-ts:.2f}s to run.')
        return result
    return timedf
