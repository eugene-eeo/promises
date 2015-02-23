from functools import wraps
from promises.utils import freeze_signature, signature,\
     validate_kwdargs, validate_posargs


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
        @wraps(freeze_signature(f))
        def function(*pos, **kwd):
            rv = f(*pos, **kwd)
            if not isinstance(rv, types):
                raise TypeError(EXPECT_RET % (types,))
            return rv
        return function
    return decorator
