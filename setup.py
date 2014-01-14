from distutils.core import setup

setup(
    name="Promises",
    version="0.0.2",
    description="Python Type Checking",
    author="Eugene Eeo",
    author_email="packwolf58@gmail.com",
    packages=["promises"],
    long_description="""
Promises is a little Python toolkit for maintaining
some sanity when doing testing or building an API in
dynamically typed languages. Easily declare the
signature of your functions like so::

    from promises import accepts, rejects

    @accepts(int)
    @rejects(int)
    def f(x):
        return x+1

Promises only exposes a very minimal declarative
and decorator-based API that is inspired by
function signatures in Go, and is very easy to
learn. You can get more documentation of the
project by visiting `github.com/eugene-eeo/promises
<https://github.com/eugene-eeo/promises>`_."""
        )

