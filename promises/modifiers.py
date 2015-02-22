class Modifier(object):
    def __init__(self, types=None):
        self.types = types

    def __getitem__(self, types):
        if not isinstance(types, tuple):
            types = (types,)
        return self.__class__(types)


class EveryMod(Modifier):
    def __instancecheck__(self, value):
        for item in self.types:
            if not isinstance(value, item):
                return False
        return True


class AnyOfMod(Modifier):
    def __instancecheck__(self, value):
        return isinstance(value, self.types)


Every = EveryMod()
AnyOf = AnyOfMod()
