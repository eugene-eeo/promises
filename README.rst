promises
========

.. image:: https://travis-ci.org/eugene-eeo/promises.png?branch=master
    :target: https://travis-ci.org/eugene-eeo/promises

.. image:: http://pypip.in/v/Promises/badge.png
    :target: https://pypy.python.org/pypi/Promises

.. image:: https://pypip.in/d/Promises/badge.png
    :target: https://pypi.python.org/pypi/Promises/

Promises is a little Python toolkit for
maintaining some sanity in dynamically
typed languages. You can easily declare
the signature of your functions using
decorators::

    from promises import accepts, returns

    # implement f(x) = x + 1
    @accepts(int)
    @returns(int)
    def f(x):
        return x+1

--------
Like it?
--------

You can install the library via pip
or just clone the github repository
in order to use it in your project::

    $ pip install Promises

-------------
Documentation
-------------

The new ``promises`` library exposes
very few functions which are deemed
necessary, and I will add more in the
future should the demand for them be
present.

~~~~~~~
accepts
~~~~~~~

The decorator takes an arbitrary
number of positional and keyword
arguments, which types will be used
to test against the passed-in objects.
Variable-name mapping is done
automatically, so no worries.::

    @accepts(list, int)
    def inc_last(array, inc=1):
        if len(array) == 0:
            array.append(0)
        array[-1] += inc

~~~~~~~
returns
~~~~~~~

Declares that the decorated function
will return a certain type, for
example::

    @returns((int, float))
    def div(x,y):
        return x/y

Note the extra braces, because ``promises``
will attempt to unpack the variables and
then match the types.

~~~~~~~
rejects
~~~~~~~

Logical complement of the ``accepts``
function, will raise a TypeError if
the passed in objects correspond to
the required types. For example, to
implement a grouping function that
forces the user to cover all possible
cases::

    @rejects(defaultdict)
    def group(g, datum):
        registry = defaultdict(list)
        for item in datum:
            for group, match in g.items():
                if match(item):
                    registry[group].append(item)
        return registry

~~~~~~~~~~
implements
~~~~~~~~~~

Declares that the argument passed in
must conform to the given trait, i.e.::

    class Copyable(object):
        copy = Method('copy')

    @implements(Copyable)
    def copy(x):
        return x

You can also pass multiple arguments
and like the ``accepts`` function it
will automatically map function arguments
to the passed in arguments::

    @implements(Copyable, int)
    def copy(x, times):
        return [x.copy for i in range(times)]

-----------------
Running the tests
-----------------

You can also run the test suite for
the current version of the promises
library by running the command below::

    $ git clone ssh://git@github.com/eugene-eeo/promises
    $ python promises/tests.py

