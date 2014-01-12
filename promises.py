from inspect import currentframe, getargvalues
from functools import wraps

def requires(*items):
    """
    Specifies that your function requires some
    keyword arguments that *must* be included
    in the function call.:

        >>> @requires("a","b")
        ... def pythagoreas(a, b):
        ...     return (a**2 + b**2) ** 0.5
        ...
        >>> pythagoreas(1,2)
        File <stdin> line ?:
            pythagoreas(1,2)
        TypeError

    param *items: Any number of names that you
                  want your wrapped function to
                  be invoked with.
    """
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            for key in items:
                if key not in kwargs:
                    raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

def returns(return_type):
    """
    Dictates that your return type is of the
    given type. This function is not recursive
    and therefore does not guaratee type
    safety within nested objects.:

        >>> @returns(int)
        ... def f(x):
        ...     return x+1
        ...
        >>> f(2)
        3
    """
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            ret = f(*args, **kwargs)
            if not isinstance(ret, return_type):
                raise TypeError
            return ret
        return inner
    return wrapper

def rejects(*positional, **named):
    """
    Allows you to specify the types of objects
    passed into your function that you want to
    refuse to accept.:

        >>> @rejects(int)
        ... def f(x):
        ...     return x**2.3
        ...
        >>> f(3)
        File <stdin> line ?:
            f(3)
        TypeError
    """
    def wrapper(f):
        argtypes = dict(zip(f.__code__.co_varnames, positional))
        argtypes.update(named)
        @wraps(f)
        def inner(*args, **kwargs):
            frame = currentframe()
            _,_,_, values = getargvalues(frame)
            for index, item in enumerate(f.__code__.co_varnames):
                argtype = argtypes.get(item)
                if isinstance(argtype, type):
                    if index < len(args):
                        if isinstance(args[index], argtype):
                            raise TypeError
                    elif item in kws:
                        if isinstance(kws[item], argtype):
                            raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

def accepts(*positional, **named):
    """
    Allows you to define what types of
    objects that your function will
    choose to handle. You may want to
    use rejects for easier inclusion::

        >>> @accepts(int) # or @accepts(x=int)
        ... def f(x):
        ...     return x
        ...
        >>> f(0.5)
        File <stdin> line ?:
            f(0.5)
        TypeError
    """
    def wrapper(f):
        argtypes = dict(zip(f.__code__.co_varnames, positional))
        argtypes.update(named)
        @wraps(f)
        def inner(*args, **kwargs):
            frame = currentframe()
            _,_,_, values = getargvalues(frame)
            for index, item in enumerate(f.__code__.co_varnames):
                argtype = argtypes.get(item)
                if isinstance(argtype, type):
                    if index < len(args):
                        if not isinstance(args[index], argtype):
                            raise TypeError
                    elif item in kws:
                        if not isinstance(kws[item], argtype):
                            raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper
