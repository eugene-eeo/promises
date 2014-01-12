from inspect import currentframe, getargvalues
from functools import wraps

def require(*items):
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            for key in items:
                if key not in kwargs:
                    raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

def returns(return_type):
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            ret = f(*args, **kwargs)
            if not isinstance(ret, return_type):
                raise TypeError
            return ret
        return inner
    return wrapper

def rejects(*positional, **named):
    def wrapper(f):
        argtypes = dict(zip(f.__code__.co_varnames, positional))
        argtypes.update(named)
        @wraps(f)
        def inner(*args, **kwargs):
            frame = currentframe()
            _,_,_, values = getargvalues(frame)
            for index, item in enumerate(f.__code__.co_varnames):
                argtype = argtypes.get(item)
                if isinstance(argtype, type):
                    if index < len(args):
                        if isinstance(args[index], argtype):
                            raise TypeError
                    elif item in kws:
                        if isinstance(kws[item], argtype):
                            raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

def accepts(*positional, **named):
    def wrapper(f):
        argtypes = dict(zip(f.__code__.co_varnames, positional))
        argtypes.update(named)
        @wraps(f)
        def inner(*args, **kwargs):
            frame = currentframe()
            _,_,_, values = getargvalues(frame)
            for index, item in enumerate(f.__code__.co_varnames):
                argtype = argtypes.get(item)
                if isinstance(argtype, type):
                    if index < len(args):
                        if not isinstance(args[index], argtype):
                            raise TypeError
                    elif item in kws:
                        if not isinstance(kws[item], argtype):
                            raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

