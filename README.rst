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

------------------
Tiny Documentation
------------------

Promises opens up four very basic
functions to you, all which effects
can be chained on one another. They
are the ``accepts``, ``returns``,
``rejects``, ``requires``, and even
``implements``. All of them raise
TypeError when the function wrapped
is invoked with the wrong arguments.

^^^^^^^
accepts
^^^^^^^

Declares that the decorated function
will accept only arguments (either
positional or keyword, it doesn't
matter during declaration) of the
particular type. For example to
implement a method that will only
accept strings::

    @accepts(str)
    def method(s):
        return

^^^^^^^
returns
^^^^^^^

Declares that your function will
only return objects of the given
type. For example to make sure
the function returns a list::

    @returns(list)
    def addone(s):
        return [i+1 for i in s]

Note that the function will not be
recursive so you can return containers
containing any object you want, just
make sure the container is of the
specified type.

^^^^^^^
rejects
^^^^^^^

Logically negative version of the
``accepts`` function, that will
accept either keyword or positional
arguments that are not of the type.
For example to implement a function
that will reject lists::

    @rejects(list)
    def func(x):
        return x

^^^^^^^^
requires
^^^^^^^^

Declares that the function requires
one or more specific keyword arguments
upon function invocation::

    @requires("name")
    def greet(name="John"):
        return "Hello %s" % (name)

^^^^^^^^^^
implements
^^^^^^^^^^

This function is inspired by the concept
of interfaces in the Go language- in which
you can pass in objects only if they
implement or have the required methods.::

    @implements("copy")
    def copy(x):
        return x.copy()

-----------------
Running the tests
-----------------

You can also run the test suite for
the current version of the promises
library by running the command below::

    $ git clone ssh://git@github.com/eugene-eeo/promises
    $ python promises/tests.py

