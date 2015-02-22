from functools import wraps


EXPECT_ARG = 'Expected argument %r to be %r'
EXPECT_RET = 'Expected return value to be %r'


def signature(f):
    if not hasattr(f, '__orgargs__'):
        code = f.__code__
        f.__orgargs__ = code.co_varnames[:code.co_argcount]
    return f.__orgargs__


def validate_posargs(args, types):
    for val, _type in zip(args, types):
        if not isinstance(val, _type):
            raise TypeError(EXPECT_ARG % (val, _type))


def validate_kwdargs(args, types):
    for arg in args:
        if arg not in types:
            continue
        value = args[arg]
        type_ = types[arg]
        if not isinstance(value, type_):
            raise TypeError(EXPECT_ARG % (value, type_))


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
