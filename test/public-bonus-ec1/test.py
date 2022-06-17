import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..')))

from parse import *

# Check that this malformed program will return an ErrorMsg object instead of an AST
with open("./test.while", "r") as fh:
    if isinstance(parse(lex("".join(fh.readlines()))), ErrorMsg):
        exit(0)
    else:
        exit(1)
