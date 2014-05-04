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
automatically, so no worries.

.. code-block:: python

    @accepts(list, int)
    def inc_last(array, inc=1):
        if len(array) == 0:
            array.append(0)
        array[-1] += inc

Note that you can now use traits
as parts of the accepted types,
so you do not need separate
decorators in order to use the
traits system:

.. code-block:: python

    @accepts(list, Each(int))
    def append_integers(array, *nums):
        for item in nums:
            array.append(item)

~~~~~~~
returns
~~~~~~~

Declares that the decorated function
will return a certain type, for
example:

.. code-block:: python

    @returns(int, float)
    def div(x,y):
        return x/y

Starting from 0.6.18 ``returns``
will start to support the usage
of traits. Note, to support return
functions that iterate through
tuples, you can do the following:

.. code-block:: python

    from promises.trait.spec import Sequence

    @returns(Sequence(int, bool))
    def is_zero(x):
        x = int(x)
        return x, x == 0

~~~~~~~
rejects
~~~~~~~

Logical complement of the ``accepts``
function, will raise a TypeError if
the passed in objects correspond to
the required types. For example, to
implement a grouping function that
forces the user to cover all possible
cases:

.. code-block:: python

    @rejects(defaultdict)
    def group(g, datum):
        registry = defaultdict(list)
        for item in datum:
            for group, match in g.items():
                if match(item):
                    registry[group].append(item)
        return registry

~~~~~~
kwonly
~~~~~~

Declares that the function will require
the given keyword arguments when calling,
if and only if they were captured by the
keyword arguments, meaning you'll have
to define some defaults.

.. code-block:: python

    @requires('config')
    def lint(config="filename"):
        # do something here

Note: If you are using Python 3, the better
way would be to use the "*" symbol, like
the following:

.. code-block:: python

    def lint(*, config="filename"):
        # do something here

As it will provide the same functionality
as the requires decorator. However you
really want to force the use of keyword
arguments, you can use the ``requires``
decorator.

~~~~~~~~
requires
~~~~~~~~

Declares that the function will require
one or more keyword arguments when invoked
regardless if they were captured. This is
a forced variant of the ``kwonly`` decorator.
For example:

.. code-block:: python

    class CombineTrait(Trait):
        combine = Method("combine")

    @accepts(CombineTrait)
    @requires("x", "y")
    def combine(x, y):
        return x.combine(y)

Another captured-variable variant of the
decorator is the ``kwonly`` decorator. It
is recommended over this if you want to
set default variables but only check captured
ones.

~~~~~~
throws
~~~~~~

Declares that the function can only throw
the specified exceptions, for example:

.. code-block:: python

    @accepts(float, float)
    @throws(ZeroDivisionError)
    def divide(x,y):
        return x/y

This is good for debugging or development
when you want to make sure that your
function throws the given exceptions.

-----------------------
Single dispatch methods
-----------------------

In Python 3, the ``functools`` library
includes the ``singledispatch`` method,
which accepts an argspec and then makes
callables which, different ones can be
called based on their type. Using that
it's possible to build PEP443_-style
generic dispatched functions. For
example:

.. code-block:: python

    from promises.trait.spec import Number
    from functools import singledispatch

    @singledispatch
    def method(x):
        pass

    @method.register(float)
    @method.register(int)
    def _(x):
        return x*2

Keep in mind that single-dispatch
generic functions do come at a cost,
especially if they are done so at
runtime, unless you use a JIT like
PyPy. Also, they do not work with
the traits in ``promises`` since
the functions do not use ``isinstance``
as a means of type checking.

.. _PEP443: https://www.python.org/dev/peps/pep-0443

If you need traits when dispatching
functions you can use the following
pattern:

.. code-block:: python

    from promises.trait.spec import Number
    from promises.dispatch import singledispatch

    @singledispatch("x")
    def f(x, y):
        pass

    @f.register(Number)
    def _(x, y):
        return x+y

    @f.register(str)
    def _(x, y):
        return str(x) + y

The semantics are almost the same as
the standard library dispatch function
except for the fact that it can dispatch
according to a given argument instead of
the first argument, reducing the need
for arg-swapping helper functions.

-----------------
Running the tests
-----------------

You can also run the test suite for
the current version of the promises
library by running the command below::

    $ git clone ssh://git@github.com/eugene-eeo/promises
    $ python promises/tests.py

