from functools import wraps
from itertools import chain
from promises.utils import *

def watch(*a, **kw):
    def inner(f):
        varnames = get_var_array(f)
        kw.update(dict(zip(varnames, a)))
        types = transform_dict(kw)

        @wraps(f)
        def wrapper(*args, **kwargs):
            context_args = True
            args = list(args)
            for index, kv in enumerate(chain(zip(varnames, args), ((0,0),), kwargs.items())):
                key, value = kv
                if key == 0:
                    context_args = False
                    continue
                if key in types:
                    value = types[key](value)
                    if context_args:
                        args[index] = value
                        continue
                    kwargs[key] = value
            return f(*args, **kwargs)
        return wrapper
    return inner
