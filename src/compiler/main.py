from laxer import laxer
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
    tokens = laxer(SOURCE_FILE)
    ast = parser(tokens)


if __name__ == '__main__':
    main()
