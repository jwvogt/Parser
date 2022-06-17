import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..')))

from parse import *


with open("./test.while", "r") as fh:
    print(fh.readlines())
    if parse(lex("".join(fh.readlines()))).run() == "120.0\n":
        exit(0)
    else:
        exit(1)
