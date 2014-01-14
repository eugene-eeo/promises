"""
    promises
    ~~~~~~~~
    Promises is a little Python toolkit for maintaining
    some sanity in dynamically typed languages. You can
    easily declare the signature of your function using
    decorators::

        >>> from promises import accepts, returns
        >>> @accepts(int)
        ... @returns(int)
        ... def f(x):
        ...     return x
"""

__all__ = [
    "implements", "accepts", "rejects",
    "requires", "returns", "exposes"
    ]
from functools import wraps

def exposes(*allowed):
    """
    Declares that the function can only be invoked
    with the given keyword arguments. This can be
    useful during tests where you may want to
    predefine some default values. Usage::

        >>> @exposes("x")
        ... def f(x):
        ...     return x
        ...
        >>> f(u=3)
        File <stdin> line ?:
            f(u=3)
        TypeError
    """
    def wrapper(f):
        if allowed == tuple('*'):
            @wraps(f)
            def function(**kwargs):
                return f(**kwargs)
            return function
        @wraps(f)
        def inner(*args, **kwargs):
            for key, value in kwargs.items():
                if key not in allowed:
                    raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

def implements(*items):
    """
    Declares that all of the objects passed into
    the function must implement the specified
    methods. This applies to all of the functions.
    Usage::

        >>> @implements("copy")
        ... def copy(x):
        ...     return x.copy()
    """
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            compl = args.__add__(tuple(kwargs.values()))
            for object_ in compl:
                for method in items:
                    if not hasattr(object_, method):
                        raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

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

def returns(*return_types):
    """
    Dictates that your return type is of the
    given type. This function is not recursive
    and therefore does not guaratee type
    safety within nested objects.:

        >>> @returns(int,float)
        ... def f(x):
        ...     return x+1
        ...
        >>> f(2)
        3
        >>> f(3.1)
        4.1
    """
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            ret = f(*args, **kwargs)
            for i in return_types:
                if isinstance(ret, i):
                    return ret
            raise TypeError
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
            length = len(args)
            for index, item in enumerate(f.__code__.co_varnames):
                argtype = argtypes.get(item)
                if isinstance(argtype, type):
                    if index < length:
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
        # map the positional arguments to the
        # required types, and make it into a
        # single large dictionary along with
        # the keyword arguments.
        argtypes = dict(zip(f.__code__.co_varnames, positional))
        argtypes.update(named)
        @wraps(f)
        def inner(*args, **kwargs):
            length = len(args)
            for index, item in enumerate(f.__code__.co_varnames):
                argtype = argtypes.get(item)
                if isinstance(argtype, type):
                    # in this case it must be a positional
                    # argument that was invoked with the
                    # function.
                    if index < length:
                        if not isinstance(args[index], argtype):
                            raise TypeError
                    elif item in kws:
                        if not isinstance(kws[item], argtype):
                            raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

