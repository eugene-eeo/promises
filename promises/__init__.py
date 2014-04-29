from functools import wraps
from itertools import chain
from collections import defaultdict
from promises.trait import Trait

obj_getter = lambda: object
__all__ = ['requires','accepts','returns','rejects',
           'throws', 'kwonly']

def accepts(*args, **kw):
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]

        tmp = {}
        tmp.update(kw)
        tmp.update(dict(zip(varnames, args)))

        types = defaultdict(obj_getter)
        for key, value in tmp.items():
            if isinstance(value, type) and issubclass(value, Trait):
                value = value()
            types[key] = value

        @wraps(f)
        def wrapper(*args, **kwargs):
            iterable = chain(zip(varnames, args), kwargs.items())
            for varname, arg in iterable:
                if not isinstance(arg, types[varname]):
                    raise TypeError
            return f(*args, **kwargs)

        return wrapper
    return function

def throws(*execptions):
    def function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as exc:
                if not isinstance(exc, execptions):
                    raise TypeError
                else:
                    raise
        return wrapper
    return function

def kwonly(*needed):
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]

        @wraps(f)
        def wrapper(*args, **kwargs):
            temp = list(kwargs.keys())
            temp.extend(map(lambda x: x[0], zip(varnames, args)))

            for item in needed:
                if item in temp and item not in kwargs:
                    raise TypeError
            return f(*args, **kwargs)
        return wrapper
    return function

def requires(*needed):
    def function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for item in needed:
                if item not in kwargs:
                    raise TypeError
            return f(*args, **kwargs)
        return wrapper
    return function

def returns(*types):
    def function(f):
        tmp = list(types)
        for item in types:
            if isinstance(item, type) and issubclass(item, Trait):
                item = item()
            tmp.append(item)

        needed = tuple(tmp)

        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if not isinstance(result, needed):
                raise TypeError
            return result

        return wrapper
    return function

def rejects(*args, **kw):
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]

        types = defaultdict(obj_getter)
        types.update(kw)
        types.update(dict(zip(varnames, args)))

        @wraps(f)
        def wrapper(*args, **kwargs):
            iterable = chain(zip(varnames, args), kwargs.items())
            for varname, arg in iterable:
                if isinstance(arg, types[varname]):
                    raise TypeError
            return f(*args, **kwargs)

        return wrapper
    return function
