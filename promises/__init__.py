"""
    promises
    ~~~~~~~~
    ``promises`` is a library for implementing
    runtime type-checking, and can be used to
    speed up development and such. A simple and
    trivial usage example::

        >>> from promises import accepts, returns
        >>> @accepts(int)
        >>> @returns(int)
        ... def add_two(x):
        ...     return x + 2
        ...
        >>> add_two(1)
        3

    More advanced constructs are available such
    as traits and single-dispatch functions,
    though you will have to look at the
    documentation for them.
"""

from functools import wraps
from itertools import chain
from collections import defaultdict

from promises.trait import Trait
from promises.utils import transform_dict, transform_iterable

obj_getter = lambda: object
__all__ = ['requires','accepts','returns','rejects',
           'throws', 'kwonly']

def accepts(*args, **kw):
    """
    The accepts decorator takes in any
    keyword and positional arguments, and
    will automatically map them to the passed
    in arguments and type-check them using
    ``isinstance`` when the wrapped function
    is invoked. For example::

        >>> @accepts(list, int)
        ... def inc_last(array, inc=1):
        ...     if len(array) == 0:
        ...         array.append(0)
        ...     array[-1] += inc
        ...
        >>> arr = []
        >>> inc_last(arr)
        >>> arr
        [1]

    Note that this function is lazy by
    design and will only type-check
    captured arguments.
    """
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]

        tmp = {}
        tmp.update(kw)
        tmp.update(dict(zip(varnames, args)))

        types = transform_dict(tmp)

        @wraps(f)
        def wrapper(*args, **kwargs):
            iterable = chain(zip(varnames, args), kwargs.items())
            for varname, arg in iterable:
                t = types[varname]
                if not isinstance(arg, t):
                    raise TypeError("{0} is not of type(s) {1}".format(arg, t))
            return f(*args, **kwargs)

        return wrapper
    return function

def throws(*exceptions):
    """
    Declares that the function can only
    throw the specified exceptions, for
    example::

        >>> @accepts(float, float)
        ... @throws(OverflowError, ZeroDivisionError)
        ... def div(x, y):
        ...     return x/y
        ...
        >>> div(1, 0)
    
    This decorator is especially useful
    when debugging to ensure a function
    only throws particular exceptions,
    for say signalling purposes.
    """
    def function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as exc:
                if not isinstance(exc, exceptions):
                    raise TypeError("{0} is not of exception(s) {1}".format(exc, exceptions))
                raise
        return wrapper
    return function

def kwonly(*needed):
    """
    Declares that the function will require
    the given keyword arguments when calling,
    if and only if they were captured by the
    keyword arguments, meaning you'll have
    to define some defaults. For example::

        >>> @requires('config')
        ... def parse(config="filename"):
        ...     with open(config) as handle:
        ...         return json.loads(handle.read())
        ...
        >>> parse(config="tmp.json")
        {"key": "value"}

    Note that you can force the use of
    specific keyword arguments when the
    function is called using the ``requires``
    decorator.
    """
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]

        @wraps(f)
        def wrapper(*args, **kwargs):
            temp = list(kwargs.keys())
            temp.extend(map(lambda x: x[0], zip(varnames, args)))

            for item in needed:
                if item in temp and item not in kwargs:
                    raise TypeError("argument {0} is not passed as a keyword argument".format(item))
            return f(*args, **kwargs)
        return wrapper
    return function

def requires(*needed):
    """
    Declares that the function will require one
    or more keyword arguments when invoked regardless
    if they were captured. This is a forced variant
    of the kwonly decorator. For example::

        >>> @accepts(Point, Point)
        ... @requires("m1","m2")
        ... def delta(m1, m2):
        ...     dx = (m2.x - m1.x) ** 2
        ...     dy = (m2.y - m1.y) ** 2
        ...     return math.sqrt((dx) + (dy))
        ...
        >>> delta(m1=Point(3,4), m2=Point(5,6))
        2.828427125

    Another captured-variable variant of the
    decorator is the kwonly decorator. It is
    recommended over this if you want to set
    default variables but only check captured
    ones.
    """
    def function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for item in needed:
                if item not in kwargs:
                    raise TypeError("{0} is a required keyword argument".format(item))
            return f(*args, **kwargs)
        return wrapper
    return function

def returns(*types):
    """
    Declares that the decorated function will
    return a certain type, for example::

        >>> @returns(int, float)
        ... def div(x,y):
        ...     return x/y
        ...
        >>> div(2,1)
        2
        >>> div(2,1.0)
        2.0

    Since ``returns`` supports trait-checking,
    you can perform type checking on functions
    which return tuples by doing something
    similar to the following::

        >>> from promises.trait.spec import Sequence
        >>> @returns(Sequence(object, bool))
        ... def get(data, key):
        ...     return data.get(key), key in data
        ...
        >>> get({}, "key")
        (None, False)

    You can read more about the traits if
    you read the documentation for the
    ``promises.trait`` and ``promises.trait.spec``
    modules.
    """
    def function(f):
        needed = transform_iterable(types)

        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if not isinstance(result, needed):
                raise TypeError("return value \"{0}\" is not of type {1}".format(result, needed))
            return result

        return wrapper
    return function

def rejects(*args, **kw):
    """
    Logical complement of the accepts function,
    will raise a ``TypeError`` if the passed in
    objects correspond to the required types.
    """
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]

        tmp = {}
        tmp.update(kw)
        tmp.update(dict(zip(varnames, args)))

        types = transform_dict(tmp)

        @wraps(f)
        def wrapper(*args, **kwargs):
            iterable = chain(zip(varnames, args), kwargs.items())
            for varname, arg in iterable:
                t = types[varname]
                if isinstance(arg, t):
                    raise TypeError("{0} shouldn't be of type {1}".format(arg, t))
            return f(*args, **kwargs)

        return wrapper
    return function
