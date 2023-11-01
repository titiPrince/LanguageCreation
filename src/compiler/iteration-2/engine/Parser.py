from .Symbols import *



NATIVES = [
    "print"
]

vartab = {}
varId = 0
equalCount = 0


def isVarNameAvailable(element, vartab):
    return element.value in vartab.keys()


def isIdNative(element):
    return element.value in NATIVES

 #    ID = 0
 #    OP = 1
 #    NUM = 2
 #    STR = 3 ["STR", truc]
 #    BOX = 4
 #    EOL = 5

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
    def scan(start, line):
        global varId
        global equalCount

        isNotBegin = bool(start)
        isBegin = not bool(start)

        if start != len(line) - 1:
            currentEl = line[start]
            nextEl = line[start + 1]
            # print(currentEl)
            # check si pas 2 "="
            if currentEl.value == Symbol.ASSIGN:
                equalCount += 1

    pass

def getAbstractTree(tokens):
    pass



