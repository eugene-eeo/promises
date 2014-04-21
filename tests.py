from promises import *
from promises.trait import *
from unittest import TestCase, main

class PromisesTestCase(TestCase):
    def test_traits(self):
        class Copyable(Trait):
            copy = Method('copy')

        @includes(Copyable)
        def ArrayLike(Trait):
            append = Method('append')
            index  = Method('index')

        @implements(Copyable)
        def copy(x):
            return x.copy()

        @implements(ArrayLike)
        def append_to_copy(x, y):
            c = x.copy()
            c.append(y)
            return c

        self.assertRaises(TypeError, copy, object)
        self.assertRaises(TypeError, append_to_copy, object)

        self.assertEqual(copy([1]), [1])
        self.assertEqual(append_to_copy([], 1), [1])

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
            return ""
        self.assertRaises(TypeError, f, 10)

    def test_accepts(self):
        @accepts(int)
        def f(x):
            return x
        self.assertRaises(TypeError, f, 1.0)
        self.assertEqual(f(8), f(x=8))

if __name__ == "__main__":
    main()

