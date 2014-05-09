"""
    promises.convert
    ~~~~~~~~~~~~~~~~

    Implements a simple type-converting decorator
    for functions that require multiple variants
    of convertible data. For example, ints to
    floats. A simple example::

        >>> from promises.convert import watch
        >>> @watch(float, float)
        ... def f(x, y):
        ...     return x+y
        ...
        >>> f(1, 2)
        3.0

    It will convert from one type to the other
    provided that the supplied argument is not
    of the target conversion type, i.e. if you
    pass in a float (or is a subclass of type
    float), it will not be converted.
"""

from functools import wraps
from itertools import chain
from promises.utils import *

__all__ = ["watch"]

def watch(*a, **kw):
    """
    Declares a watched function that will
    automatically convert types of the
    different instance. For example, to
    force float division:

        >>> @watch(float, float)
        ... def f(x, y):
        ...     return x/y
        ...
        >>> f(1, 1)
        1.0

    Note that it only converts from types
    that are unlike. For example, if you
    pass in a float it will not be converted.
    Like the other ``accepts`` and ``rejects``
    decorators it will automatically map
    function to names.
    """
    def inner(f):
        varnames = get_var_array(f)
        kw.update(dict(zip(varnames, a)))
        types = transform_dict(kw)

        @wraps(f)
        def wrapper(*args, **kwargs):
            context_args = True
            args = list(args)
            for index, kv in enumerate(chain(zip(varnames, args), ((0,0),), kwargs.items())):
                key, value = kv
                if key == 0:
                    context_args = False
                    continue
                if key in types:
                    needed = types[key]
                    if not isinstance(value, needed):
                        value = needed(value)
                        if context_args:
                            args[index] = value
                            continue
                        kwargs[key] = value
            return f(*args, **kwargs)
        return wrapper
    return inner
