"""
    promises.trait.impl
    ~~~~~~~~~~~~~~~~~~~
    A metaprogramming-based generic-type definition
    module for the ``@implements`` function. Example
    usage::

        >>> from promises.trait.impl import List
        >>> @returns(list)
        ... @implements(List, List)
        ... def join(x, y):
        ...     temp = []
        ...     for iterable in (x,y):
        ...         for item in iterable:
        ...             temp.append(item)
        ...     return temp
        ...
        >>> join([1,2], [3,4])
        [1, 2, 3, 4]

    Generic types do respond to isinstance calls
    after the ``__instancecheck__`` hook was made
    in the ``Trait`` class.
"""

from promises.trait.impl import *

__all__ = ["List","Stack","Dictionary","Collection"]

class MetaBuilder(object):
    def __new__(self, methods=[], attrs=[]):
        cls = type("Generic", (Trait,), {})
        for selector, iterable in ((Method, methods), (Attribute, attrs)):
            for item in iterable:
                setattr(cls, item.strip("__"), selector(item))

        return cls

_ITEMS = MetaBuilder(methods=["__setitem__","__delitem__","__getitem__"])

@includes(_ITEMS)
@includes(MetaBuilder(methods=["__iter__"]))
class List(Trait):
    """
    A generic ``List`` type that needs the
    object to implement the following
    attributes:

     - ``__delitem__``, ``__setitem__``, and ``__getitem__``
     - ``remove`` and ``sort``
     - ``__iter__``
    """
    remove = Method("remove")
    sort   = Method("sort")

@includes(List)
class Stack(Trait):
    """
    The generic stack trait includes all of
    the definitions from the ``List`` trait
    but needs to implement more functions:

     - ``push``
     - ``pop``
    """
    push = Method("push")
    pop  = Method("pop")

@includes(MetaBuilder(methods=["__iter__","__contains__"]))
@includes(_ITEMS)
class Dictionary(Trait):
    """
    A dictionary trait only has a few requirements,
    in particular the ``__*item__``, ``__contains__``,
    and ``__iter__`` methods, since these are the
    commonly used methods of a dict-like object.
    """
    pass

@includes(Dictionary)
class Collection(Trait):
    """
    A collection is a more advanced version of a
    dictionary that will implement the following
    functions:

     - ``pop``
     - ``keys``
     - ``update``
     - ``values``
    """
    pop    = Method("pop")
    keys   = Method("keys")
    update = Method("update")
    values = Method("values")

class Each(object):
    """
    A metaclass which produces a new generic
    type of class ``Trait`` which validates
    iterables. In particular, every object
    within the iterable must conform to the
    type specified. For example, to implement
    a function that saves all MongoEngine
    documents::

        >>> from promises.trait.spec import Each
        >>> from promises import implements
        >>> @implements(Each(Document))
        ... def save_all(*docs):
        ...     for item in docs:
        ...         item.save()
        ...

    :param typename: Any number of types or
        traits that you want to be able to
        implement.
    """
    def __new__(self, *typename):
        new = type("generic-each", (Trait,), {})
        def valid(ins, x):
            for item in x:
                if not isinstance(item, typename):
                    return False
            return True
        new.__instancecheck__ = valid
        return new

