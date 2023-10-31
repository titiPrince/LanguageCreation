from re import match
from Symbols import *



class TokenType:
    ID = 0
    OP = 1
    NUM = 2
    STR = 3
    BOX = 4
    EOL = 5


class Token:
    def __init__(self, _type, _value):
        self.type = _type
        self.value = _value

    def __str__(self):
        return "TOKEN : Type = " + str(self.type) + " ; Value = " + str(self.value)

def scan(start: int, chars: str, regex: str) -> tuple[str, int]:
    """
    Scan the **chars** from the **start** index to find a word who respect the **regex**
    :param start: The index where starting to search in **chars** with the **regex**.
    :param chars: The String where search for the **regex**.
    :param regex: The **regex** to search for.
    :return: [**word**: str, **end**: int] The **word** found by the regex and the index of the word's **end**.
    """

    cChars = len(chars)

    for i in range(start, cChars):
        char = chars[i]

        if not match(regex, char):
            return (chars[start:i], i - start - 1)

    return (chars[start:cChars], cChars - start - 1)


def lexer(script: str) -> list[Token]:
    """
    Transform the script input to a list of tokens.
    :param script: The script input of the compiler.
    """

    _range = range(len(script))

    for i in _range:
        char: str = script[i]

        if char in Symbol.OPERATIONS:
            pass

        elif char in Symbol.