import re

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


def scan(start, line, regex):
    for i in range(start, len(line)):
        char = line[i]

        if not re.match(regex, char):
            return [line[start:i], i - start - 1]

    return [line[start:len(line)], len(line) - start - 1]


def main():
    tokens = []

    file = open(SOURCE_FILE, "r")
    source = file.read()
    file.close()

    lines = source.split(";")

    for line in lines:
        instruction = ()
        skip = 0

        for i, c in enumerate(line):
            if skip > 0:
                skip -= 1

            elif c in " \n":
                continue

            elif c in "+-/*:=":
                tokens.append(("op", c))

            elif re.match("[_a-zA-Z]", c):
                word, skip = scan(i, line, "[_a-zA-Z]")
                tokens.append(("id", word))

            elif re.match("[.0-9]", c):
                word, skip = scan(i, line, "[.0-9]")
                tokens.append(("num", word))

            else:
                raise Exception("Character not allowed")

    print(tokens)


if __name__ == '__main__':
    main()
