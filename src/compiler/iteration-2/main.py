import sys
import os

from engine.Lexer import *
from engine import Parser
from engine.Transpiler import *


if __name__ == '__main__':
    nargs = len(sys.argv)

    if nargs < 2:
        raise Exception("One argument is missing.")

    if nargs > 3:
        raise Exception("Too many arguments.")

    source = sys.argv[1]
    destination = source + ".o"

    if not os.path.exists(source):
        raise Exception("The source file doesn't exists.")

    if nargs == 2:
        destination = sys.argv[2]

    sourceFile = open(source, "r")

    script = sourceFile.read()

    sourceFile.close()

    tokens = lexer(script)
    errors = Parser.verifySyntax(tokens)

    if not errors:
        ast = Parser.getAbstractTree(tokens)
        languageC = ast.transpile()

        destFile = open(source + ".c", "w")
        destFile.write(languageC)
        destFile.close()

        os.system("gcc " + source + ".c -o " + destination)
        os.remove(source + ".c")

        os.system("./" + destination)

    else:
        raise Exception("\n".join(errors))
