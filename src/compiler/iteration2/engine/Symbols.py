class TokenType:
    ID = "ID"
    OP = "OP"
    NUM = "NUM"
    STR = "STR"
    BOX = "BOX"
    SEP = "SEP"


class Token:
    count = 0

    def __init__(self, _type, _value):
        self.id: int = Token.count
        self.type: str = _type
        self.value: str | int = _value

        Token.count += 1

    def __str__(self):
        return f"{self.id:03d} - T{f'[{self.type}]': <5} - {str(self.value)}"


class Symbol:
    ASSIGN = "="

    EQUAL = "=="
    NEQUAL = "!="
    GREATER = ">"
    GREQUAL = ">="
    LOWER = "<"
    LOEQUAL = "<="

    AND = "et"
    OR = "ou"
    NOT = "non"

    MUL = "*"
    ADD = "+"
    SUB = "-"
    DIV = "/"
    MOD = "%"
    OPERATIONS = "+-*/%=><!"
    CALCS = "+-*/%"

    QUOT = '"'
    PARS = "("
    PARE = ")"
    ACOS = "{"
    ACOE = "}"
    EOL = ";"
    SEP = ","
    BOXES = "(){}"

    IGNORES = " \n"

    IF = "si"
    ELSEIF = "etsi"
    ELSE = "sinon"

    FOR = "pour"
    FORCOND = "quand"
    FORSTEP = "incr"

    FCT_PRINT = "print"


class Symbols:
    CONDITIONS = (Symbol.EQUAL, Symbol.NEQUAL, Symbol.GREATER, Symbol.GREQUAL, Symbol.LOWER, Symbol.LOEQUAL)
    CALCULATIONS = (Symbol.ADD, Symbol.MUL, Symbol.SUB, Symbol.DIV, Symbol.MOD)
    OPERATORS = (Symbol.ADD, Symbol.MUL, Symbol.SUB, Symbol.DIV, Symbol.MOD, Symbol.ASSIGN, Symbol.GREATER, Symbol.LOWER)
    GATES = (Symbol.AND, Symbol.OR)
    ENDS = (Symbol.SEP, Symbol.EOL)
