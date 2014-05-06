from promises.trait import Trait
from collections import defaultdict

OBJ_GETTER = lambda: object
IS_TRAIT   = lambda x: isinstance(x, type) and issubclass(x, Trait)

def transform_dict(dictionary):
    tmp = defaultdict(OBJ_GETTER)
    for key, value in dictionary.items():
        if IS_TRAIT(value):
            value = value()
        tmp[key] = value
    return tmp

def transform_iterable(iterable):
    return tuple((i() if IS_TRAIT(i) else i) for i in iterable)
