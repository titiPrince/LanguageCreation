class TokenType:
	ID = "ID"
	OP = "OP"
	NUM = "NUM"
	STR = "STR"
	BOX = "BOX"
	EOL = "EOL"


class Token:
	def __init__(self, _type, _value):
		self.type = _type
		self.value = _value

	def __str__(self):
		return "TOKEN [" + str(self.type) + "]	= \"" + str(self.value) + "\""

#   ID = 0
#   OP = 1
#   NUM = 2
#   STR = 3 ["STR", truc]
#   BOX = 4
#   EOL = 5

class Symbol:
	ASSIGN = "="

	EQUAL = "=="
	NEQUAL = "!="
	GREATER = ">"
	GREQUAL = ">="
	LOWER = "<"
	LOEQUAL= "<="

	AND = "and"
	OR = "or"
	NOT = "not"

	MUL = "*"
	ADD = "+"
	SUB = "-"
	DIV = "/"
	OPERATIONS = "+-*/=><!"

	QUOT = '"'
	PARS = "("
	PARE = ")"
	ACOS = "{"
	ACOE = "}"
	EOL = ";"
	BOXES = "(){}"

	IGNORES = " \n"
