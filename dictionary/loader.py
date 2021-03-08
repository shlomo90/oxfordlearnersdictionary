from sites.oxfordlearners import Oxfordlearners


class DictionaryLoader(object):
    SITES_LIST = {"ox": Oxfordlearners, }

    def __init__(self):
        pass

    def get_module(self, name):
        return self.SITES_LIST.get(name, None)
