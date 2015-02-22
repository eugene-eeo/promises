from pytest import raises
from collections import Sequence, Mapping
from promises import accepts, returns, Every, AnyOf


def test_anyof():
    assert isinstance(100, AnyOf[int,float])
    assert isinstance(1.0, AnyOf[int,float])


def test_every():
    assert isinstance({}, Every[Mapping,dict])
    assert isinstance([], Every[Sequence,list])


@accepts(AnyOf[int,float], int)
@returns(str)
def f(x, index, container=str):
    return container(x)[index:]


def test_signature():
    g = returns(str)(f)
    assert f.__orgargs__ == ('x', 'index', 'container')
    assert g.__orgargs__ == f.__orgargs__


def test_accepts():
    assert f(100, 0) == '100'
    assert f(1.0, 1) == '.0'

    callbacks = [
        lambda: f(2, 1.0),
        lambda: f('', index=1),
        lambda: f(1, index=2.0),
        lambda: f(x='', index=''),
    ]

    for item in callbacks:
        with raises(TypeError):
            item()


def test_returns():
    with raises(TypeError):
        f(1.0, 1, lambda x: [x])
