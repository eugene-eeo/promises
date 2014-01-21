from promises import *
from unittest import TestCase, main

class PromisesTestCase(TestCase):
    def test_throws(self):
        @throws(ValueError)
        def f(x):
            if x < 0:
                raise ValueError
            raise OSError
        self.assertRaises(RuntimeError, f, 2)
        self.assertRaises(ValueError, f, -1)

    def test_disallows(self):
        @disallows("x")
        def f(x):
            return x+1
        self.assertRaises(TypeError, f, x=1)
        self.assertEqual(f(1), 2)

        @disallows("*")
        def f(x, u=1):
            return x+u
        self.assertRaises(TypeError, f, x=1)
        self.assertEqual(f(1), 2)

    def test_exposes(self):
        @returns(int)
        @exposes("x")
        def f(x):
            return x+1
        self.assertEqual(f(3), 4)
        self.assertRaises(TypeError, f, u=1)

        @exposes("*")
        def f(x):
            return x+1
        self.assertEqual(f(x=2), 3)
        self.assertRaises(TypeError, f, 2)

    def test_implements(self):
        @implements("copy")
        def f(x):
            "Basic stuff"
            return x.copy()
        self.assertRaises(TypeError, f, 5)
        self.assertEqual(f.__doc__, "Basic stuff")

    def test_rejects(self):
        @rejects(float)
        def a(x):
            "Basic stuff"
            return 0
        self.assertRaises(TypeError, a, 4.0)
        self.assertEqual(a(2), a(x=2))
        self.assertEqual(a.__doc__, "Basic stuff")

    def test_require(self):
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

