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
    for argname in args:
        if argname not in types:
            continue
        expected = types[argname]
        if not isinstance(args[argname], expected):
            raise TypeError(EXPECT_ARG % (argname, expected))


def accepts(*types, **index):
    def decorator(f):
        sig = getargs(f.__code__).args
        index.update(zip(sig, types))

        @wraps(f)
        def function(*pos, **kwd):
            validate_posargs(sig, pos, index)
            validate_kwdargs(kwd, index)
            return f(*pos, **kwd)
        return function
    return decorator


def returns(*types):
    def decorator(f):
        @wraps(f)
        def function(*pos, **kwd):
            rv = f(*pos, **kwd)
            if not isinstance(rv, types):
                raise TypeError(EXPECT_RET % (types,))
            return rv
        return function
    return decorator
