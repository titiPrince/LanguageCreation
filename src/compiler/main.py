from lexer import lexer
from parserErrorHandler import parser
from transpiler import transpile

SOURCE_FILE = "test"

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
    print(errors)

    if not errors:
        transpile(tokens)

    # si des erreur son presentes dans le code

    else:

        pass

if __name__ == '__main__':
    main()
