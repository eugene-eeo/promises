promises
========

Promises is a little Python toolkit for
maintaining some sanity in dynamically
typed languages. You can easily declare
the signature of your functions using
decorators:

```python
from promises import accepts, returns

# implement f(x) = x + 1
@accepts(int)
@returns(int)
def f(x):
  return x+1
```

In it's current iteration, promises
is a very simple and naive library
that will not determine how rightfully
invoked your function is when faced
with keyword arguments.

You can also run the test suite for
the current version of the promises
library by running the command below:

```bash
$ python promises/tests.py
```

