from collections import defaultdict


class Implementation(object):
    def __init__(self, obj):
        self.obj = obj
        self.requirements = []
        self.methods = []
        self.types = {}

    def configure(self, options):
        requirements = options.get('attributes')
        if requirements:
            for item in requirements:
                self.requirements.append(item)

        types = options.get('types')
        if types:
            self.types.update(types)

        methods = options.get('methods')
        if methods:
            for item in methods:
                self.methods.append(item)

    def require(self, item):
        self.requirements.append(item)

    def validate(self, obj):
        if not isinstance(obj, self.obj):
            return False

        for item in self.requirements:
            if not hasattr(obj, item):
                return False

        for key, value in self.types.items():
            if not hasattr(obj, key) or\
               not isinstance(getattr(obj, key),value):
                return False

        for item in self.methods:
            if not hasattr(obj, item) or\
               not callable(getattr(obj, item)):
                return False
        return True

