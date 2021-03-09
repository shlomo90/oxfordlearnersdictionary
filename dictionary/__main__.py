import sys
from enum import Enum
from error import print_error_msg, ERRNUM
from loader import DictionaryLoader


ARGS = Enum("PY", "WORD", "TYPE", "MAX", AVAILABLE=2)


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
