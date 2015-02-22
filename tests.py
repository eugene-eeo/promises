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
