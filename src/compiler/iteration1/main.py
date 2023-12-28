import os

from lexer import lexer
from parserErrorHandler import parser
from transpiler import transpile

SOURCE_FILE = "v1"

"""
[
    ["id", "a"],
    ["op", "="],
    ["num", "5"],

    ["id", "b"],
    ["op", "="],
    ["num", "10"],

    ["id", "c"],
    ["op", "="],
    ["id", "a"],
    ["op", "+"],
    ["id", "b"],
    ["op", "+"],
    ["num", "1"]

    ["id", "print"],
    ["op", ":"],
    ["id", "c"]
]
"""


def main():
    tokens = lexer(SOURCE_FILE)
    errors = parser(tokens)

    if not errors:
        c = transpile(tokens)

        with open(SOURCE_FILE + ".c", "w") as file:
            file.write(c)

        os.system("gcc " + SOURCE_FILE + ".c -o " + SOURCE_FILE + ".o")
        # os.remove(SOURCE_FILE + ".c")

        os.system("./" + SOURCE_FILE + ".o")

    else:
        print(errors)

if __name__ == '__main__':
    main()
