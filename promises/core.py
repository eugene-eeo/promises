from functools import wraps
from promises.utils import signature, validate_kwdargs, validate_posargs


EXPECT_ARG = 'Expected argument %r to be %r'
EXPECT_RET = 'Expected return value to be %r'


def accepts(*types, **index):
    def decorator(f):
        sig = signature(f)
        index.update(zip(sig, types))

        @wraps(f)
        def function(*pos, **kwd):
            validate_posargs(pos, types)
            validate_kwdargs(kwd, index)
            return f(*pos, **kwd)
        return function
    return decorator


def returns(*types):
    def decorator(f):
        signature(f)

        @wraps(f)
        def function(*pos, **kwd):
            rv = f(*pos, **kwd)
            if not isinstance(rv, types):
                raise TypeError(EXPECT_RET % (types,))
            return rv
        return function
    return decorator
