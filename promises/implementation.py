"""
    promises.implementation
    ~~~~~~~~~~~~~~~~~~~~~~~
    Adds an abstraction atop typical attribute
    and function validation to make validating
    objects against desired implementations
    really simple.
"""

from collections import defaultdict


class Implementation(object):
    """
    Represents a single Implementation.
    Usage is something of the following::

        >>> from promises.implementation import Implementation
        >>> impl = Implementation(list)
        >>> impl.configure({
        ...     'methods':['append','index']
        ... })

    :param obj: The type to provide a
        wrapper around, or an object
        that must not have been instantiated.
    """
    def __init__(self, obj):
        self.obj = obj
        self.requirements = []
        self.methods = []
        self.types = {}

    def configure(self, options):
        """
        Configures the Implementation object
        by quickly assigning and mapping the
        passed in variables to the internal
        representations. Usage::

            >>> impl.configure({
            ...     'methods':    ['fetch','bark'],
            ...     'attributes': ['owner','name'],
            ...     'types': {
            ...         'owner': Person,
            ...         'name':  str
            ...     }
            ... })

        It accepts a dictionary of options
        that may contain three keys- first
        ``attributes``, which is a list of
        attributes that objects must have.

        Secondly, it is the ``methods`` key,
        which is a list of methods that the
        object must have. They are like
        attributes but must be callable.

        Lastly is the types dictionary,
        which takes in a dictionary of
        attribute-to-type pairs that the
        object must also refrain to.
        """
        requirements = options.get('attributes')
        if requirements:
            for item in requirements:
                self.requirements.append(item)

        types = options.get('types')
        if types:
            self.types.update(types)

        methods = options.get('methods')
        if methods:
            for item in methods:
                self.methods.append(item)

    def require(self, item, mode="a"):
        """
        Takes in two arguments, one required
        and one defaulting to "a". It assigns
        the passed in object to the internal
        storage based on the mode specified.
        Example usage::

            >>> impl.require('index')
            >>> impl.requirements
            ['index']
            >>> impl.require('index', mode="m")
            >>> impl.methods
            ['index']
            >>> impl.require({'index':int}, mode='t')
            >>> impl.types
            {'index':int}

        Below is a list of mode (passed in
        as a string) to object types:

         - **a**: A string containing a
            required attribute name.
         - **t**: A dictionary containing
            attribute-name to type mapping(s).
         - **m**: A string contatining a
            required method name.
        """
        if mode == 'a':
            self.requirements.append(item)
            return
        elif mode == 't':
            self.types.update(item)
            return
        self.methods.append(item)
        return

    def validate(self, obj):
        """
        Validates a given object based on
        the internal configuration. Usage
        example::

            >>> dog = Doge()
            >>> impl = Implementation(Doge)
            >>> impl.configure({
            ...     'methods':['bark','sit']
            ... })
            >>> impl.validate(dog)
            True
        """
        if not isinstance(obj, self.obj):
            return False

        for item in self.requirements:
            if not hasattr(obj, item):
                return False

        for key, value in self.types.items():
            if not hasattr(obj, key) or\
               not isinstance(getattr(obj, key),value):
                return False

        for item in self.methods:
            if not hasattr(obj, item) or\
               not callable(getattr(obj, item)):
                return False
        return True

