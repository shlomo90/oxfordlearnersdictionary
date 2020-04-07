# General Import
import sys, os, re
import requests
import json

# My code Import
from enum import Enum
from error import ERRNUM, ERRMSG, DictionaryError, print_error_msg


ARGS = Enum("PY", "WORD", "TYPE", "MAX", AVAILABLE=2)


class DictionaryLoader(object):
    LOAD_DIR = "./dictionary_modules"
    LOAD_PATH = "dictionary_modules."

    def __init__(self):
        self.load_mods = {}
        for load_mod_file in os.listdir(self.LOAD_DIR):
            # 0 is file name without extension ('.py')
            load_mod = self.LOAD_PATH + load_mod_file.split('.')[0]
            self.load_mods[load_mod] = __import__(load_mod, fromlist=[load_mod])

    def _extract_module_name(self, mod):
        return str(mod).split('.')[-1]

    def get_module(self, name):
        for mod in self.load_mods.keys():
            mod_name = self._extract_module_name(mod)
            if re.match("^{}".format(name), mod_name):
                cls = eval("self.load_mods[mod].{}".format(mod_name.capitalize()))
                return cls
        return None


def parse_arguements(args):
    if len(args) < ARGS.AVAILABLE:
        print_error_msg(ERRNUM.E_ARGS)

    word = args[ARGS.WORD]
    try:
        module = args[ARGS.TYPE]
    except IndexError:
        module = 'ox'   # default module
    return (word, module)


if __name__ == "__main__":
    word, module = parse_arguements(sys.argv)
    loader = DictionaryLoader()
    cls = loader.get_module(module)
    if cls is None:
        print_error_msg(ERRNUM.E_NODICT)
        exit(1)

    word_inst = cls().find_word(word)
    word_inst.show_word()
