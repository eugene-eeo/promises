"""
    promises.trait.impl
    ~~~~~~~~~~~~~~~~~~~
    Implements the ``Trait`` class and associated
    helper methods like the ``includes``, ``Attribute``,
    and ``Method`` functions. General usage::

        >>> from promises.trait.impl import *
        >>> class MyTrait(Trait):
        ...     meth = Method("meth-name")
        ...

    For the generic type definitions you may want
    to browse the code in ``promises.trait.spec``.
"""

__all__ = ["Attribute","Method","Trait","includes"]

Attribute = lambda x: lambda z, ins: hasattr(ins, x)
Method    = lambda x: lambda z, ins: hasattr(ins, x) and callable(getattr(ins,x))

class Trait(object):
    """
    A Trait object represents a set of
    attributes or functions that an
    object will have to implement in
    order to be validated by the given
    trait. For example a trait for a
    string would be::

        >>> class String(Trait):
        ...     getslice = Method("__getslice__")
        ...     rsplit = Method("rsplit")
        ...

    Note that the names of the instance/
    class variables need not to correspond
    to anything. They are just variables,
    and can hold a function which validates
    the object. The constructor also needs
    to accept zero arguments.
    """
    def __validate__(self, obj):
        """
        Validates a given object according
        to the callbacks assigned to each
        of the attributes not starting
        with a "__" and is basically a
        short-circuiting validator like
        the "and" operator and returns
        either True or False. Example
        usage::

            >>> trait.__validate__(obj)
            True

        :param obj: The object to validate
            against the trait.
        """
        for item in dir(self):
            if not item.startswith('__'):
                required = getattr(self, item)
                if isinstance(required, Trait):
                    required = lambda x: hasattr(x, item) and required.validate(x)

                if not required(obj):
                    return False
        return True

def includes(*traits):
    """
    A decorator to expand the definition
    of the decorated trait by including
    all definitions specified in the
    included trait. For example:

        >>> from promises.trait.spec import Stack
        >>> @includes(Stack)
        ... class StackQueue(Trait):
        ...     put = Method("put")
        ...     get = Method("get")
        ...

    However it is important to note that
    due to Python 2's bound function
    semantics, the included instance
    will called.

    :param traits: Any number of traits
        to include in the decorated
        trait.
    """
    def function(cls):
        for trait in traits:
            instance = trait()
            for item in dir(trait):
                if not item.startswith('__'):
                    setattr(cls, item, getattr(instance, item))
        return cls
    return function
