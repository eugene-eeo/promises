from functools import wraps
from itertools import chain
from promises.trait import Trait

__all__ = ['implements','requires','accepts','returns','rejects']

def implements(*args, **types):
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]
        types.update(dict(zip(varnames, args)))

        @wraps(f)
        def wrapper(*args, **kwargs):
            iterable = chain(zip(varnames, args), kwargs.items())
            for varname, arg in iterable:
                if varname in types and\
                    not Trait.__validate__(types[varname], arg):
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
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if not isinstance(result, types):
                raise TypeError
            return result
        return wrapper
    return function

def rejects(*args, **types):
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]
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

def accepts(*args, **types):
    def function(f):
        code = f.__code__
        varnames = code.co_varnames[:code.co_argcount]
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
