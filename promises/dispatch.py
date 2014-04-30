"""
    promises.dispatch
    ~~~~~~~~~~~~~~~~~
    Single dispatch functions meant for use in
    Python 2 libraries where ``functools.singledispatch``
    is not available or you want traits to be
    supported. Usage example::

        >>> from promises.dispatch import singledispatch
        >>> @singledispatch
        ... def f(x):
        ...     pass
        ...
        >>> @f.register(int)
        >>> def _(x):
        ...     return x+1
        ...
        >>> f({})
        >>> f(1)
        2

    Note that this library tries to mock the
    standard library dispatch functions as
    much as possible in terms of interface
    and standard API, but implementation is
    vastly different as we are using the
    slower but more powerful ``isinstance``
    function to determine delegates.
"""

from functools import wraps
from collections import defaultdict
from promises.trait.impl import Trait

__all__ = ["singledispatch"]

def generic_register(f):
    """
    Returns a closure that registers a given
    type/trait to the function's meta object.
    Usage example::

        >>> register = generic_register(dispatched_f)
        >>> @register(int)
        ... def _(x):
        ...     return x+1
        ...
        >>> dispatched_f(1)
        2

    Note that the returned function is meant
    for use as a decorator and therefore you
    should use it as so.
    """
    def closure(typename):
        def wrapper(g):
            ty = typename
            if isinstance(typename, type) and\
                    issubclass(typename, Trait):
                ty = typename()
            f.meta.registered[ty] = g
            return g
        return wrapper
    return closure

def singledispatch(f):
    """
    A generic single-dispatch function decorator;
    the decorated function will have the ``meta``
    attribute as a storage mechanism and the
    returned function has a ``register`` function
    which can be used to register types for
    delegation. For example::

        >>> @singledispatch
        ... def f(x):
        ...     pass
        ...
        >>> @f.register(int)
        ... @f.register(float)
        ... def _(x):
        ...     return x+1
        ...
        >>> f(True)
        >>> f(1)
        2

    If type implementations for a given
    argument are not found, the function
    will not raise a ``NotImplementedError``,
    instead it will return the result of
    the decorated function (which will
    always be called regardless of
    implementation availability).
    """
    code = f.__code__
    varnames = code.co_varnames[:code.co_argcount]

    def wrapper(*args, **kwargs):
        # check if arguments are okay before
        # we do any processing
        res = f(*args, **kwargs)
        if len(args) < 1:
            first = kwargs[varnames[0]]
        else:
            first = args[0]

        for typename, delegate in f.meta.registered.items():
            if isinstance(first, typename):
                return delegate(*args, **kwargs)
        return res

    f.meta = type("generic-meta", (object,), {})
    f.meta.registered = defaultdict(lambda: f)
    wrapper.register = generic_register(f)
    return wrapper

