from .Symbols import *
from .Transpiler import *
from .VarManager import *



NATIVES = [
	"print",
	"si",
	"sinon",
	"etsi",
	"pour",
	"et",
	"ou",
	"quand",
	"inc",
]


def isVarNameAvailable(element, vartab):
	return element.value in vartab.keys()


def isIdNative(element):
	return element.value in NATIVES







# if
# (
# truc
# =
# 2
# )
# {
# print
# :
# 1
# }
# else
# (
# print
# :
# )
# ;

# for( i = 0 ; i < )


isIf = False
isFor = False
# is begin d'une instruction de base ou d'une instruction dans des {}
isBegin= True
isNotBegin = False

vartab = {"si":-3,"sinon":-2,"etsi":-1}
varId = 0
equalCount = 0

def scan( tokens):
	global varId
	global equalCount
	global isBegin
	global isNotBegin
	bracketCount= 0
	parenthesisCount =0


	# defini si c'est le debut d'une intruction

	for i in range(len(tokens)-1):
		currentEl = tokens[i]
		nextEl = tokens[i + 1]
		print(currentEl.type)
		# # index 0 de l'iteration
		if currentEl.type is TokenType.BOX and currentEl.value == "{":
			bracketCount += 1
		elif currentEl.type is TokenType.BOX and currentEl.value == "}":
			bracketCount -= 1
		elif currentEl.type is TokenType.BOX and currentEl.value == "(":
			parenthesisCount += 1
		elif currentEl.type is TokenType.BOX and currentEl.value == ")":
			parenthesisCount -= 1

		if parenthesisCount<0:
			return "Syntax error: incorect symbol ')'  "
		if bracketCount < 0:
			return "Syntax error: incorect symbol '}'  "




		if i == 0 and (
				currentEl.type is TokenType.OP or
				currentEl.type is TokenType.BOX or
				currentEl.type is TokenType.STR or
				currentEl.type is TokenType.SEP or
				currentEl.type is TokenType.NUM
		):
			return "tu fait pas d'effort dès le premier charactère"

		if ((currentEl.type is TokenType.STR)
				and not (nextEl.value == "(" or nextEl.value == ")" or nextEl.value == "{" or nextEl.value == "}" or nextEl.value == ";" or nextEl.type is TokenType.OP or  nextEl.value == "et" or  nextEl.value == "ou")):
				and not (la
			return "Error Syntax: String:"+ currentEl.value + " is follow by a false stateùe,nt"
		#
		#  si la fonction native est en première place elle DOIT etre suivi de (
		elif currentEl.type is TokenType.ID and isIdNative(currentEl) and not nextEl.value is Symbol.PARS and isBegin and currentEl.value == "print":
			return "Error Syntax: A native function must be follow by '('"

		#
		# # si la varible n'existe pas dans vartab et n'est pas en 1ere position
		# elif (currentEl.type is TokenType.ID and not isIdNative(currentEl) and not isVarNameAvailable(currentEl, vartab)
		# 		and isNotBegin):
		# 	print(isNotBegin)
		# 	return "Error Syntax: la varible '" + currentEl.value + "' n'est pas defini : token :"+ str(i)
		# # si la variable est en position 1 elle doit etre suivi d'un "=" (asignation ou delcaration)
		# elif (currentEl.type is TokenType.ID and not isIdNative(currentEl) and nextEl.value != "=" and isBegin ):
		# 	return "Error Syntax: la varible '" + currentEl.value + "' n'est pas suivi d'un '='"
		#
		# # en debut d'unstruction push le n
		# if isVarNameAvailable(currentEl, vartab) == False and isIdNative(currentEl) == False and isBegin and currentEl.value != "}":
		# 	varId += 1
		# 	vartab[currentEl.value] = varId
		# print(vartab)
		#
		#
		# if(isBegin and currentEl.value != "}"):
		# 	isBegin = False
		# 	isNotBegin = True
		# elif currentEl.value == ";" or currentEl.value=="}":
		# 	isBegin = True
		# 	isNotBegin = False
		#
		#


def scanInstruction(tokens: list[Token]) -> tuple[int, LiteralNumber | VarReading | BinaryOperation | VarAssignation]:
	lastParam = None
	currentParam = None

	skip = 0

	for i, token in enumerate(tokens):
		# Token detection
		match token.type:
			case TokenType.ID:
				currentParam = VarReading(token.value)

			case TokenType.OP:
				if token.value == Symbol.ASSIGN:
					currentParam = VarAssignation()

			case TokenType.NUM:
				break

			case TokenType.STR:
				break

			case TokenType.BOX:
				break

			case TokenType.SEP:
				break

		# Instruction assembler
		if lastParam is None:
			lastParam = currentParam

		elif isinstance(currentParam, VarAssignation):
			currentParam.setName(lastParam.name)
			lastParam = currentParam




def scanCondition(tokens: list[Token]) -> tuple[int, Condition]:
	lastParam = None
	currentParam = None

	for i, token in enumerate(tokens):
		# Token detection
		match token.type:
			case TokenType.ID:
				if token.value in (Symbol.AND, Symbol.NOT, Symbol.OR):
					currentParam = BoolComparison(token.value)

				else:
					currentParam = VarReading(token.value)

			case TokenType.OP:
				if token.value in Symbol.CALCS:
					currentParam = BinaryOperation(token.value)

				else:
					currentParam = Condition(token.value)

			case TokenType.NUM:
				currentParam = LiteralNumber(token.value)

			case TokenType.STR:
				currentParam = LiteralString(token.value)

			case TokenType.BOX:
				if token.value == Symbol.ACOS:
					return i, lastParam

		# Condition assembler
		if lastParam is None:
			lastParam = currentParam

		elif isinstance(lastParam, (Condition, BoolComparison)):
			lastParam.setB(currentParam)

		elif isinstance(currentParam, (Condition, BoolComparison)):
			currentParam.setA(lastParam)
			lastParam = currentParam


def scanIfStatement(tokens: list[Token]) -> tuple[int, IfStatement]:
	# Main
	ptrCondition, condition = scanCondition(tokens)
	ptrBlock, block = scanBlock(tokens[ptrCondition+1:])

	statement = IfStatement(condition, block)

	token = tokens[ptrBlock + 1]
	pointer = ptrBlock + 1

	# Else if
	while token.value == Symbol.ELSEIF:
		ptrElseIfCondition, elseIfCondition = scanCondition(tokens[pointer + 1:])
		ptrElseIfBlock, elseIfBlock = scanBlock(tokens[ptrElseIfCondition + 1:])

		statement.addElifBranch(ElseIfStatement(elseIfCondition, elseIfBlock))

		token = tokens[ptrElseIfBlock + 1]
		pointer = ptrElseIfBlock + 1

	# Else
	if token == Symbol.ELSE:
		ptrElseBlock, elseBlock = scanBlock(tokens[pointer + 1:])

		statement.elseBranch = ElseStatement(elseBlock)

		pointer = ptrElseBlock + 1

	return pointer, statement


def scanForLoop(tokens: list[Token]) -> tuple[int, ForLoop]:
	var = tokens[0].value

	ptrCondition, condition = scanCondition(tokens[1:])
	ptrIncr, incr = scanInstruction(tokens[ptrCondition + 2:])
	ptrBlock, block = scanBlock(tokens[ptrIncr + 1:])

	statement = ForLoop(var, condition, incr, block)

	return ptrBlock, statement


def scanFunctionParameters(tokens: list[Token]) -> tuple[int, list[LiteralNumber | LiteralString | VarReading | BinaryOperation]]:
	parameters = []
	lastParam = None
	currentParam = None

	for i, token in enumerate(tokens):
		# Token detection
		match token.type:
			case TokenType.ID:
				# Add here in the future, condition to verify if there is a function call

				currentParam = VarReading(token.value)

			case TokenType.NUM:
				currentParam = LiteralNumber(token.value)

			case TokenType.STR:
				currentParam = LiteralString(token.value)

			case TokenType.OP:
				if token.value in Symbols.CONDITIONS:
					currentParam = Condition(token.value)

				elif token.value in Symbol.CALCS:
					currentParam = BinaryOperation(token.value)

				elif token.value in Symbols.GATES:
					currentParam = BoolComparison(token.value)

			case TokenType.BOX:
				if token.value == Symbol.PARE:
					return i, parameters

			case TokenType.SEP:
				currentParam = None

		# Condition assembler
		if lastParam is None:
			lastParam = currentParam

		elif currentParam is None:
			parameters.append(lastParam)
			lastParam = None

		elif isinstance(lastParam, (Condition, BoolComparison)):
			lastParam.setB(currentParam)

		elif isinstance(currentParam, (Condition, BoolComparison)):
			currentParam.setA(lastParam)
			lastParam = currentParam


def scanBlock(tokens: list[Token]) -> tuple[int, Block]:
	block = Block()

	for i, token in enumerate(tokens):
		if token.value == Symbol.IF:
			ptrIfStatement, ifStatementBlock = scanIfStatement(tokens[i + 1:])

		elif token.value == Symbol.FOR:
			ptrForLoop, forLoopBlock = scanForLoop(tokens[i + 1:])

		elif token.value == Symbol.FCT_PRINT:
			ptrFunctionParams, functionParameters = scanFunctionParameters(tokens[i + 2:]) # +2 to skip the (

		elif token.value == Symbol.ACOE:
			return i, block


def getAbstractTree(tokens: list[Token]) -> AbstractSyntaxTree:
	for i, token in enumerate(tokens):
		if skip > 0:
			skip = skip - 1
			continue

		match token.type:
			case TokenType.ID:
				break

			case TokenType.OP:
				break

			case TokenType.NUM:
				break

			case TokenType.STR:
				break

			case TokenType.BOX:
				break

			case TokenType.SEP:
				stackInstruction = []

	return ast