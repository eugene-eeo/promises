promises
========

.. image:: https://travis-ci.org/eugene-eeo/promises.png?branch=master
    :target: https://travis-ci.org/eugene-eeo/promises

.. image:: http://pypip.in/v/Promises/badge.png
    :target: https://pypy.python.org/pypi/Promises

.. image:: https://pypip.in/d/Promises/badge.png
    :target: https://pypi.python.org/pypi/Promises/

Promises is a simple Python library for the runtime
enforcement of types during function calls. It has
the unfortunate fate of being the same name as the
Javascript pattern. Usage examples:

.. code-block:: python

    @accepts(AnyOf[int,float])
    @returns(str)
    def f(x):
        return str(x)

Note the ``getitem`` magic implemented in the ``AnyOf``
pseudo-type. These pseudo-types can be combined like
logical operators to create long, hard-to-grok type
signatures. The current iteration of Promises hopes
to streamline the library from it's previous cluttered
state.
