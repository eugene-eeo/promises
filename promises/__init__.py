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
    "requires", "returns", "exposes",
    "disallows", "throws"
    ]
from functools import wraps

ARG_NOT_EXPOSED  = "Named argument {0} is not exposed."
ARG_IS_REQUIRED  = "The argument {0} is required."
MUST_NOT_BE_TYPE = "Argument {0} must not be of type {1}."
MUST_RETURN_TYPE = "Function must return type[s]: {0}."
MUST_ACCEPT_TYPE = "Argument {1} must be of type {1}."
DOESNT_IMPLEMENT = "Object doesn't implement method {0}."
EXCEPTION_TYPE   = "Raised exception must be of type {0}."

def throws(*exceptions):
    """
    Declares that the function can only
    raise the supplied exceptions- any
    other raised will cause in a RuntimeError.
    This is only useful but isn't used
    solely for testing. Usage example::

        >>> @throws(ValueError)
        ... def f(div):
        ...     if div == 0:
        ...         raise ValueError
        ...     return 5/div

    You may not want to actually use this
    signature in production since it is
    actually quite slow (exception handling
    does come at a price!).
    """
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as err:
                # apparently we cannot just do ``err in
                # exceptions`` since the err variables is
                # an instance
                if not isinstance(err, exceptions):
                    raise RuntimeError(EXCEPTION_TYPE.format(exceptions))
                raise
        return inner
    return wrapper

def disallows(*not_allowed):
    """
    Declares that the wrapped function doesn't
    allow any keyword arguments of the given
    name- the logical negation of ``exposes``.
    Usage example::

        >>> @disallows('bits')
        ... def f(bits=0):
        ...     return file.read(bits)

    Similar to the exposes function, if the
    "*" is the only argument passed in, the
    decorator will return a function that
    will only take in positional arguments.
    """
    def wrapper(f):
        if not_allowed == ('*',):
            @wraps(f)
            def inner(*args):
                return f(*args)
            return inner
        @wraps(f)
        def inner(*args, **kwargs):
            for key, value in kwargs.items():
                if key in not_allowed:
                    raise TypeError(ARG_NOT_EXPOSED.format(key))
            return f(*args, **kwargs)
        return inner
    return wrapper

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

    If "*" is the only passed in argument, this
    decorator will return a function that can only
    be called with keyword arguments.
    """
    def wrapper(f):
        if allowed == ('*',):
            @wraps(f)
            def inner(**kwargs):
                return f(**kwargs)
            return inner
        @wraps(f)
        def inner(*args, **kwargs):
            for key, _ in kwargs.items():
                if key not in allowed:
                    raise TypeError(ARG_NOT_EXPOSED.format(key))
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
                        raise TypeError(DOESNT_IMPLEMENT.format(method))
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
                    raise TypeError(ARG_IS_REQUIRED.format(key))
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
            if isinstance(ret, return_types):
                return ret
            raise TypeError(MUST_RETURN_TYPE.format(return_types))
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
        varnames = f.__code__.co_varnames
        argtypes = dict(zip(varnames, positional))
        argtypes.update(named)
        @wraps(f)
        def inner(*args, **kwargs):
            length = len(args)
            for index, item in enumerate(varnames):
                argtype = argtypes.get(item)
                if argtype is not None:
                    if index < length:
                        if isinstance(args[index], argtype):
                            raise TypeError(
                                    MUST_NOT_BE_TYPE.format(item, argtype)
                                    )
                    elif item in kwargs:
                        if isinstance(kwargs[item], argtype):
                            raise TypeError(
                                    MUST_NOT_BE_TYPE.format(item, argtype)
                                    )
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
        accepted = f.__code__.co_varnames
        argtypes = dict(zip(accepted, positional))
        argtypes.update(named)
        @wraps(f)
        def inner(*args, **kwargs):
            length = len(args)
            for index, item in enumerate(accepted):
                argtype = argtypes.get(item)
                if argtype is not None:
                    if index < length:
                        if not isinstance(args[index], argtype):
                            raise TypeError(
                                    MUST_ACCEPT_TYPE.format(item, argtype)
                                    )
                    elif item in kwargs:
                        if not isinstance(kwargs[item], argtype):
                            raise TypeError(
                                    MUST_ACCEPT_TYPE.format(item, argtype)
                                    )
            return f(*args, **kwargs)
        return inner
    return wrapper

