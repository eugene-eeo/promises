from functools import wraps
from inspect import getargs
from itertools import chain


EXPECT_ARG = 'Expected argument [%s] to be %r'
EXPECT_RET = 'Expected return value to be %r'


def validate_posargs(sig, args, types):
    for name, val, _type in zip(sig, args, types):
        expected = types[name]
        if not isinstance(val, expected):
            raise TypeError(EXPECT_ARG % (name, expected))


def validate_kwdargs(args, types):
    for argname in set(args).intersection(types):
        expected = types[argname]
        if not isinstance(args[argname], expected):
            raise TypeError(EXPECT_ARG % (argname, expected))


def accepts(*types, **kws):
    def decorator(f):
        sig = getargs(f.__code__).args
        kws.update(zip(sig, types))

        @wraps(f)
        def function(*pos, **kwd):
            validate_posargs(sig, pos, kws)
            validate_kwdargs(kwd, kws)
            return f(*pos, **kwd)
        return function
    return decorator


def returns(*types):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            rv = f(*args, **kwargs)
            if not isinstance(rv, types):
                raise TypeError(EXPECT_RET % (types,))
            return rv
        return function
    return decorator
