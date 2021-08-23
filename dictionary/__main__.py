import sys
from enum import Enum
from error import print_error_msg, ERRNUM
from loader import DictionaryLoader


# ex: python -m "name"
# ex: python -m "name" "ox"
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
    dict_ins = DictionaryLoader.get_module(module)
    dict_ins.find_word(word).show_word()
