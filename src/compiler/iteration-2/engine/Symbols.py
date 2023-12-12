class TokenType:
	ID = "ID"
	OP = "OP"
	NUM = "NUM"
	STR = "STR"
	BOX = "BOX"
	SEP = "SEP"


class Token:
	def __init__(self, _type, _value):
		self.type = _type
		self.value = _value

	def __str__(self):
		return "TOKEN [" + str(self.type) + "]	-> " + str(self.value)


class Symbol:
	ASSIGN = "="

	EQUAL = "=="
	NEQUAL = "!="
	GREATER = ">"
	GREQUAL = ">="
	LOWER = "<"
	LOEQUAL= "<="

	AND = "et"
	OR = "ou"
	NOT = "non"

	MUL = "*"
	ADD = "+"
	SUB = "-"
	DIV = "/"
	OPERATIONS = "+-*/=><!"
	CALCS = "+-*/"

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