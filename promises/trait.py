
Attribute = lambda x: lambda ins: hasattr(ins, x)
Method    = lambda x: lambda ins: hasattr(ins, x) and callable(getattr(ins,x))
Object    = lambda x, trait: lambda ins: hasattr(ins, x) and Trait.__validate__(x, trait)

class Trait(object):
    def __validate__(trait, obj):
        for item in dir(trait):
            if not item.startswith('__'):
                required = getattr(trait, item)
                if isinstance(required, Trait):
                    required = lambda x: Trait.__validate__(required, x)

                if not required(obj):
                    return False
        return True

def includes(*traits):
    def function(cls):
        for trait in traits:
            for item in dir(trait):
                if not item.startswith('__'):
                    setattr(cls, item, getattr(trait, item))
    return function
