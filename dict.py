#!./ox/bin/python

import sys, os, re
import requests
import json

from error import ERRNUM, ERRMSG, DictionaryError
from enum import Enum


ARGS = Enum("PY", "WORD", "TYPE", "MAX", AVAILABLE=2)


class DictionaryLoader(object):
    LOADABLE = {}
    LOAD_DIR = "./dictionaries"
    LOAD_PATH = "dictionaries."

    def __init__(self):
        self.load_mods = {}
        for load_mod_file in os.listdir(self.LOAD_DIR):
            load_mod = load_mod_file.split('.')[0]
            load_mod = self.LOAD_PATH + load_mod
            self.load_mods[load_mod] = __import__(load_mod, fromlist=[load_mod])

    def load_dictionary(self, name):
        if name in self.load_mods:
            pass

    def list_dictionary(self):
        return self.load_mods.keys()

    def get_dictionary(self, name):
        for mod in self.load_mods.keys():
            mod_name = self._extract_module_name(mod)
            if re.match("^{}".format(name), mod_name):
                cls = eval("self.load_mods[mod].{}".format(mod_name.capitalize()))
                return cls

        return None

    def _extract_module_name(self, mod):
        return str(mod).split('.')[-1]


if __name__ == "__main__":
    if len(sys.argv) < ARGS.AVAILABLE:
        print "Need argument."
        exit(1)

    loader = DictionaryLoader()
    target_word = sys.argv[ARGS.WORD]
    # Default is oxfordlearners
    target_dict = 'ox'
    if len(sys.argv) == ARGS.MAX:
        target_dict = sys.argv[ARGS.TYPE]

    dict_cls = loader.get_dictionary(target_dict)
    if dict_cls is None:
        raise DictionaryError("No Dictionary")

    dict_inst = dict_cls()
    word = dict_inst.find_word(target_word)
