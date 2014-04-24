from promises.trait.impl import *

__all__ = ["List","Stack","Dictionary","Collection"]

class MetaBuilder(object):
    def __new__(self, methods=[], attrs=[]):
        cls = type("Generic", (Trait,), {})
        for selector, iterable in ((Method, methods), (Attribute, attrs)):
            for item in iterable:
                setattr(cls, item.strip("__"), selector(item))

        return cls

_ITEMS = MetaBuilder(methods=["__setitem__","__delitem__"])

@includes(_ITEMS)
@includes(MetaBuilder(methods=["__iter__"]))
class List(Trait):
    remove = Method("remove")
    sort   = Method("sort")

@includes(List)
class Stack(Trait):
    push = Method("push")
    pop  = Method("pop")

@includes(_ITEMS)
@includes(MetaBuilder(methods=["__getitem__"]))
class Dictionary(Trait):
    pass

@includes(Dictionary)
class Collection(Trait):
    pop    = Method("pop")
    keys   = Method("keys")
    update = Method("update")
    values = Method("values")
