from re import match
from classes import Token, TokenType


def scan(start, line, regex):
    for i in range(start, len(line)):
        char = line[i]

        if not match(regex, char):
            return [line[start:i], i - start - 1]

    return [line[start:len(line)], len(line) - start - 1]


def lexer(source_file):
    tokens = []

    file = open(source_file, "r")
    source = file.read()
    file.close()

    lines = source.split(";")[0:-1]

    for line in lines:
        skip = 0

        for i, c in enumerate(line):
            if skip > 0:
                skip -= 1

            elif c in " \n":
                continue

            elif c in "+-/*:=":
                tokens.append(Token(TokenType.OP, c))

            elif match("[_a-zA-Z]", c):
                word, skip = scan(i, line, "[_a-zA-Z]")
                tokens.append(Token(TokenType.ID, word))

            elif match("[.0-9]", c):
                word, skip = scan(i, line, "[.0-9]")
                tokens.append(Token(TokenType.NUM, word))

            else:
                raise Exception("Character not allowed")

        tokens.append(Token(TokenType.EOL, 0))

    # Make list of line
    line = []
    lines = []

    for token in tokens:
        line.append(token)

        if token.type == TokenType.EOL:
            lines.append(line)
            line = []

    return lines
