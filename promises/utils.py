EXPECT_ARG = 'Expected argument %s (%r) to be %r'


def freeze_signature(f):
    if not hasattr(f, '__orgargs__'):
        code = f.__code__
        f.__orgargs__ = code.co_varnames[:code.co_argcount]
    return f


def signature(f):
    return freeze_signature(f).__orgargs__


def validate_posargs(args, types):
    for idx, pair in enumerate(zip(args, types), 1):
        val, type_ = pair
        if not isinstance(val, type_):
            raise TypeError(EXPECT_ARG % (idx, val, type_))


def validate_kwdargs(args, types):
    for arg in args:
        if arg not in types:
            continue
        val, type_ = args[arg], types[arg]
        if not isinstance(value, type_):
            raise TypeError(EXPECT_ARG % (arg, val, type_))
