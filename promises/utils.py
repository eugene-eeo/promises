from promises.trait import Trait
from collections import defaultdict

OBJ_GETTER = lambda: object
IS_TRAIT   = lambda x: isinstance(x, type) and issubclass(x, Trait)

__all__ = ['transform_dict','transform_iterable','get_var_array']

def transform_dict(dictionary):
    tmp = defaultdict(OBJ_GETTER)
    for key, value in dictionary.items():
        if IS_TRAIT(value):
            value = value()
        tmp[key] = value
    return tmp

def transform_iterable(iterable):
    return tuple((i() if IS_TRAIT(i) else i) for i in iterable)

def get_var_array(f):
    code = f.__code__
    return code.co_varnames[:code.co_argcount]
