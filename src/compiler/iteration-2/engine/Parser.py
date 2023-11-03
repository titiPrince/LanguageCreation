from .Symbols import *
from .Transpiler import *



NATIVES = [
	"print"
]


def isVarNameAvailable(element, vartab):
	return element.value in vartab.keys()


def isIdNative(element):
	return element.value in NATIVES


isIf = False
isFor = False


vartab = {}
varId = 0
equalCount = 0





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

def verifySyntax(tokens):
	pass
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


# def scan(start, tokens):
# 	global varId
# 	global equalCount
#
# 	reset = True
# 	for i in range(len(tokens)):
# 		currentEl = tokens[start]
# 		nextEl = tokens[start + 1]
#
		# # index 0 de l'iteration
		# if i == 0 and (
		# 	currentEl.type == TokenType.OP or
		# 	currentEl.type == TokenType.BOX or
		# 	currentEl.type == TokenType.STR or
		# 	currentEl.type == TokenType.EOL or
		# 	currentEl.type == TokenType.NUM
		# ):
		# 	return "tu fait pas d'effort dès le premier charactère"
		#
		# 	#  si la fonction native est en première place elle DOIT etre suivi de (
		# elif currentEl.type == TokenType.ID and isIdNative(currentEl) and not nextEl.value == Symbol.PARS:
		# 	return "Error Syntax: A native function must be follow by ':'"
		#
		#
		# #
		# # si la varible n'existe pas dans vartab et n'est pas en 1ere position
		# elif currentEl.type == TokenType.ID and not isIdNative(currentEl) and not isVarNameAvailable(currentEl,vartab):
		# #
		# # 	return "Error Syntax: la varible '" + currentEl.value + "' n'est pas defini"
		# #
		# # # si la variable est en position 1 elle doit etre suivi d'un "=" (asignation ou delcaration)
		# # elif currentEl.type == TokenType.ID and not isIdNative(currentEl) and nextEl.value != "=" and isBegin:
		# # 	return "Error Syntax: la varible '" + currentEl.value + "' n'est pas suivi d'un '='"
		#
		# if(reset and (
		# 	   currentEl.value == Symbol.ASSIGN or
		# 	   currentEl.value == Symbol.ASSIGN
		# 		)
		# )


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
			skip -= 1
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