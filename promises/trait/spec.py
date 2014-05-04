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

from sys import version_info
from promises.trait.impl import *

__all__ = ["List","Stack","Dictionary","Collection","Each","Sequence"]

class MetaBuilder(object):
    def __new__(self, methods=[], attrs=[]):
        cls = type("Generic", (Trait,), {})
        for selector, iterable in ((Method, methods), (Attribute, attrs)):
            for item in iterable:
                setattr(cls, item.strip("__"), selector(item))

        return cls

ITEMS = MetaBuilder(methods=["__iter__","__setitem__","__delitem__",
                             "__getitem__","__contains__"])

@includes(ITEMS)
class List(Trait):
    """
    A generic ``List`` type that needs the
    object to implement the following
    attributes:

     - ``__delitem__``, ``__setitem__``, and ``__getitem__``
     - ``insert`` and ``index``
     - ``__contains__``
     - ``__iter__``
    """
    insert = Method("insert")
    index  = Method("index")

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

@includes(ITEMS)
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
        >>> from promises import accepts
        >>> @accepts(Each(Document))
        ... def save_all(*docs):
        ...     for item in docs:
        ...         item.save()
        ...
        >>> save_all(docs)

    :param typename: Any number of types or
        traits that you want to be able to
        implement.
    """
    def __new__(self, *typename):
        def valid(ins, x):
            for item in x:
                if not isinstance(item, typename):
                    return False
            return True
        data = {"__instancecheck__": valid}
        new = type("generic-each", (Trait,), data)
        return new

NUM = (float, complex, int)

class Number(Trait):
    """
    A generic ``Number`` type that validates
    any instance of ``long``, ``float``,
    ``int``, or ``complex``. However, take
    note that ``long`` is only available in
    Python 2.x. Use this in type checked
    functions that accept/return numerical
    types::

        >>> from promises.trait.spec import Number
        >>> from promises import accepts
        >>> @accepts(Number)
        ... def f(x):
        ...     return x+1

    This trait subclass does not perform
    any of the expected method/attribute
    checking, but will just validate based
    on the instance type.
    """
    typecheck = lambda self, x: isinstance(x, NUM)
    if version_info[0] == 2:
        typecheck = lambda self, x: isinstance(x, NUM + (long,))

class Sequence(Trait):
    """
    A sequence is a trait that validates
    a datum based on the types of items passed
    in, and assumes that the datum must be of
    type ``tuple``. For example:

        >>> from promises.trait.spec import Sequence
        >>> from promises import accepts
        >>> @accepts(Sequence(int, int))
        ... def add_tuple(x):
        ...     return x[0]+x[1]
        ...
        >>> add_tuple((1,2))
        3

    Note that the constructor method
    doesn't return a ``Sequence``
    trait but returns a generic trait.

    :param types: An arbitrary number of
        types that can be passed to the
        constructor method.
    """
    def __new__(self, *types):
        types = tuple((i() if isinstance(i, type) and issubclass(i, Trait) else i) for i in types)
        length = len(types)
        def function(ins, datum):
            if not (type(datum) is tuple):
                return False

            counter = 0
            for index, item in enumerate(zip(types, datum)):
                needed, got = item
                if not isinstance(got, needed):
                    return False
                counter += 1
            return True

        data = {"__instancecheck__": function}
        return type("generic-sequence", (Trait,), data)

