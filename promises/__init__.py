from functools import wraps
from itertools import chain
from collections import defaultdict

__all__ = ['implements','requires','accepts','returns','rejects']

obj_getter = lambda: object

def implements(*args, **kw):
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]

        types = {}
        types.update(dict(zip(varnames, args)))
        types.update(kw)

        types = {i:k() for i,k in types.items()}

        @wraps(f)
        def wrapper(*args, **kwargs):
            iterable = chain(zip(varnames, args), kwargs.items())
            for varname, arg in iterable:
                if varname in types and not types[varname].__validate__(arg):
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
        length = len(types)
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if hasattr(result, '__iter__'):
                counter = 0
                for res, required in zip(result, types):
                    if not isinstance(res, required):
                        raise TypeError
                    counter += 1
                if counter != length:
                    raise TypeError

            else:
                if not isinstance(result, types):
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

def accepts(*args, **kw):
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
                if not isinstance(arg, types[varname]):
                    raise TypeError
            return f(*args, **kwargs)

        return wrapper
    return function
