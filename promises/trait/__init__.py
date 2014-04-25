"""
    promises.trait
    ~~~~~~~~~~~~~~
    Implements a ``Trait`` class similar to the one
    found in the Rust type system, and can be used to
    build modular dependencies for the type system.
    Generic types are available from ``promises.trait.spec``
    but only include definititions for a Collection,
    Dictionary, Stack, and a List. Usage examples::

        >>> from promises import implements
        >>> from promises.trait import *
        >>> class DataType(Trait):
        ...     name = Attribute('name')
        ...     addr = Attribute('addr')
        ...     store = Method('store')
        ...
        >>> @implements(DataType)
        ... def name_and_addr_of(obj):
        ...     return obj.name, obj.addr
        ...

    An example use case for generic types to implement
    a counter incrementing function that operates on
    dict-like objects::

        >>> from promises.trait.spec import Dictionary
        >>> @implements(Dictionary)
        ... def increment(data, key):
        ...     data[key] += 1
        ...     return data[key]
        ...
        >>> increment({"a":0}, "a")
        1
        >>> from collections import defaultdict
        >>> increment(defaultdict(int), "a")
        1

    Finally, an example situation in which the ``includes``
    function can be used to make modular traits for
    use throughout a program/library during testing::

        >>> from promises.trait.spec import Dictionary
        >>> @includes(Dictionary)
        ... class Mapping(Trait):
        ...     # define some requirements here
        ...
"""

from promises.trait.impl import Trait, includes
