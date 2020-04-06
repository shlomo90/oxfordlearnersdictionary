class Enum(object):
    def __init__(self, *args, **kwargs):
        self.enum = {}
        for i, arg in enumerate(args):
            self.enum[arg] = i

        for key, value in kwargs.iteritems():
            if type(value) is not int:
                raise TypeError("Type should be int.")
            self.enum[key] = value

    def __getattr__(self, name):
        if name in self.enum:
            return self.enum[name]
        else:
            return None
