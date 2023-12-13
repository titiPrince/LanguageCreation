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
