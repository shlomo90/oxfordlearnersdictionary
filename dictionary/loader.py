from sites.oxfordlearners import Oxfordlearners


SITES_LIST = {"ox": Oxfordlearners, }


class DictionaryLoader(object):

    def __init__(self):
        pass

    @classmethod
    def get_module(cls, name):
        if name not in SITES_LIST:
            return Oxfordlearners()
        else:
            return SITES_LIST[name]()
