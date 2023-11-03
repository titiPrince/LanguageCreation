from .Symbols import *
from .Transpiler import *



NATIVES = [
	"print"
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

# def verifySyntax(tokens):
# 	print('coucou')
#
# 	return scan(0,tokens)
# def areBracketsValid(tokens):
# 	countBrackets = 0
# 	for i in tokens:
# 		if i.value== "{" :
# 			countBrackets+=1
# 		elif i.value== "}":
# 			countBrackets-=1
# 	return True if countBrackets == 0  else False
# def areParenthesisValid(tokens):
# 	countParentesises = 0
# 	for i in tokens:
# 		if i.value== "(" :
# 			countParentesises+=1
# 		elif i.value== ")":
# 			countParentesises-=1
# 	return True if countParentesises == 0  else False

isIf = False
isFor = False
# is begin d'une instruction de base ou d'une instruction dans des {}
isBegin= True
isNotBegin = False

vartab = {}
varId = 0
equalCount = 0

def scan(start, tokens):
	global varId
	global equalCount
	global isBegin
	global isNotBegin
	bracketCount= 0
	parenthesisCount =0


	# defini si c'est le debut d'une intruction
	start = 0
	for i in range(len(tokens)):
		currentEl = tokens[start]
		nextEl = tokens[start + 1]
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
			currentEl.type is TokenType.EOL or
			currentEl.type is TokenType.NUM
		):
			return "tu fait pas d'effort dès le premier charactère"

		#  si la fonction native est en première place elle DOIT etre suivi de (
		elif currentEl.type is TokenType.ID and isIdNative(currentEl) and not nextEl.value is Symbol.PARS and isBegin:
			return "Error Syntax: A native function must be follow by '('"


		# si la varible n'existe pas dans vartab et n'est pas en 1ere position
		elif currentEl.type is TokenType.ID and not isIdNative(currentEl) and not isVarNameAvailable(currentEl,vartab) and isNotBegin:

			return "Error Syntax: la varible '" + currentEl.value + "' n'est pas defini"

		# si la variable est en position 1 elle doit etre suivi d'un "=" (asignation ou delcaration)
		elif currentEl.type is TokenType.ID and not isIdNative(currentEl) and nextEl.value != "=" and isBegin:
			return "Error Syntax: la varible '" + currentEl.value + "' n'est pas suivi d'un '='"



		if(isBegin):
			isBegin = False
			isNotBegin = True
		elif currentEl.value == ";":
			isBegin = True
			isNotBegin = False
		print(isBegin)

def getAbstractTree(tokens: list[Token]) -> AbstractSyntaxTree:
	def scanBranch(tokens: list[Token]) -> tuple[int, list[Instruction]]:
		return tuple()

	def isVarDeclared(name: str) -> bool:
		return name in declaredVar.keys()

	def getLastStack():
		if inCondition:
			return stackCondition[-1] if stackCondition else None
		return stackInstruction[-1] if stackInstruction else None

	ast = AbstractSyntaxTree()

	declaredVar = {}

	instruction = None
	stackInstruction = []

	inCondition = False
	stackCondition = []

	skip = 0

	for i, token in enumerate(tokens):
		if skip > 0:
			skip = skip - 1
			continue

		match (token.type):
			case TokenType.ID:
				if token.value in [Symbol.IF, Symbol.ELSEIF]:
					inCondition = True
					stackCondition = []

				elif token.value is Symbol.ELSE:
					pass

				elif token.value in [Symbol.FOR, Symbol.FORCOND, Symbol.FORSTEP]:
					pass

				else:
					if inCondition:
						stackCondition.append(VarReading(token.value))

					else:
						if isVarDeclared(token.value):
							instruction = VarAssignation(token.value)

						else:
							instruction = VarDeclaration(token.value)

				break

			case TokenType.OP:
				if token.value is Symbol.EQUAL:
					if inCondition:
						pass

					else:
						continue

				elif token.value in Symbol.CALCS:
					lastStack = getLastStack()

					if isinstance(lastStack, BinaryOperation):
						lastStack.setB(BinaryOperation(token.value, lastStack.b))

					else:
						stackInstruction.append(LiteralNumber(token.value))

				break

			case TokenType.NUM:
				if inCondition:
					pass

				else:
					lastStack = getLastStack()

					if isinstance(lastStack, BinaryOperation):
						lastStack.setB(LiteralNumber(token.value))

					else:
						stackInstruction.append(LiteralNumber(token.value))

			case TokenType.STR:
				break

			case TokenType.BOX:
				break

			case TokenType.EOL:
				stackInstruction = []

	return ast