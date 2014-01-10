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
        @wraps(f)
        def inner(*args, **kwargs):
            for key, value in zip(args, positional):
                if isinstance(key, value):
                    raise TypeError
            for key, value in kwargs.items():
                needed = named.get(key)
                if needed and isinstance(value, needed):
                    raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

def accepts(*positional, **named):
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            for key, value in zip(positional, args):
                if not isinstance(value, key):
                    raise TypeError
            for key, value in kwargs.items():
                needed = named.get(key)
                if needed and not isinstance(value, needed):
                    raise TypeError
            return f(*args, **kwargs)
        return inner
    return wrapper

