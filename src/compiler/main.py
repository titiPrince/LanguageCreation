from lexer import laxer
from parser import parser

SOURCE_FILE = "code"

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
    ast = parser(tokens)

    print(ast)


if __name__ == '__main__':
    main()
