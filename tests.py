from promises import *
from promises.trait import spec
from collections import defaultdict
from unittest import TestCase, main

class TraitsTestCase(TestCase):
    def test_each(self):
        @returns(int)
        @accepts(spec.Each(int))
        def sum_int(*x):
            return sum(x)

        self.assertRaises(TypeError, sum_int, "x")
        self.assertEqual(sum_int(1,2,3), 6)

    def test_dictionary(self):
        @returns(int)
        @accepts(data=spec.Dictionary)
        def increment_key(data, key, inc=1):
            data[key] += inc
            return data[key]

        a = defaultdict(int)
        self.assertEqual(increment_key(a, "a"), 1)

    def test_list(self):
        @accepts(data=spec.List)
        def increment_index(data, index, inc=1):
            data[index] += inc
            return data[index]

        a = [0]
        self.assertEqual(increment_index(a, 0), 1)

class PromisesTestCase(TestCase):
    def test_throws(self):
        @accepts(Exception)
        @throws(IOError, OSError)
        def ioerror_raiser(exc):
            raise exc

        self.assertRaises(TypeError, ioerror_raiser, NameError)
        self.assertRaises(OSError, ioerror_raiser, OSError)

    def test_traits(self):
        class Countable(Trait):
            count = Method('count')

        class ArrayLike(Trait):
            append = Method('append')
            index  = Method('index')

        includes(Countable)(ArrayLike)

        @accepts(Countable)
        def count(x):
            return x.count(1)

        @accepts(ArrayLike)
        def append(x, y):
            x.append(y)
            return x

        self.assertRaises(TypeError, count, object)
        self.assertRaises(TypeError, append, object)

        self.assertEqual(count([1]), 1)
        self.assertEqual(append([], 1), [1])

    def test_rejects(self):
        @rejects(float)
        def a(x):
            "Basic stuff"
            return 0
        self.assertRaises(TypeError, a, 4.0)
        self.assertEqual(a(2), a(x=2))
        self.assertEqual(a.__doc__, "Basic stuff")

    def test_requires(self):
        @requires("node")
        def f(node):
            return ""
        self.assertRaises(TypeError, f, 10)
        self.assertEqual(f(node=2), "")

    def test_returns(self):
        @returns(int)
        def f(x):
            return x
        self.assertRaises(TypeError, f, "")
        self.assertEqual(1, f(1))

        @returns((int, bool))
        def f(x):
            return 1, False
        self.assertEqual(f(10), (1, False))

    def test_accepts(self):
        @accepts(int)
        def f(x):
            return x
        self.assertRaises(TypeError, f, 1.0)
        self.assertEqual(f(8), f(x=8))

if __name__ == "__main__":
    main()

