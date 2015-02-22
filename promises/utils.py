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
