
Attribute = lambda x: lambda z, ins: hasattr(ins, x)
Method    = lambda x: lambda z, ins: hasattr(ins, x) and callable(getattr(ins,x))

class Trait(object):
    def __validate__(self, obj):
        for item in dir(self):
            if not item.startswith('__'):
                required = getattr(self, item)
                if isinstance(required, Trait):
                    required = lambda x: hasattr(x, item) and required.validate(x)

                if not required(obj):
                    return False
        return True

def includes(*traits):
    def function(cls):
        for trait in traits:
            instance = trait()
            for item in dir(trait):
                if not item.startswith('__'):
                    setattr(cls, item, getattr(instance, item))
        return cls
    return function
