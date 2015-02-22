from collections import Sequence, Mapping
from pytest import raises
from promises import accepts, returns, Every, AnyOf


def test_anyof():
    assert isinstance(100, AnyOf[int,float])
    assert isinstance(1.0, AnyOf[int,float])


def test_every():
    assert isinstance({}, Every[Mapping,dict])
    assert isinstance([], Every[Sequence,list])


def test_accepts():
    @accepts(int, y=int, z=str)
    def function(x, y, z=''):
        pass

    function(1, 2, '')
    function(1, y=2, z='')

    with raises(TypeError):
        function(1, y='', z='')


def test_returns():
    @returns(AnyOf[float,int])
    def f(x):
        return x + 1

    assert f(1) == 2
    assert f(1.0) == 2.0

    with raises(TypeError):
        f('')


def test_accepts_decorated():
    @accepts(AnyOf[int,float])
    @returns(str)
    def f(x):
        return str(x)

    assert f(100) == '100'
    assert f(1.0) == '1.0'

    with raises(TypeError):
        f('')

    with raises(TypeError):
        f(x='')
