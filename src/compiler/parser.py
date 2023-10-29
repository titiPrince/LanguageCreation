from classes import TokenType

"""
[
    ["id", "a"],
    ["op", "="],
    ["num", "5"],

    ["eol", 0],

    ["id", "b"],
    ["op", "="],
    ["num", "10"],

    ["eol", 0],

    ["id", "c"],
    ["op", "="],
    ["id", "a"],
    ["op", "+"],
    ["id", "b"],
    ["op", "+"],
    ["num", "1"],

    ["eol", 0],

    ["id", "c"],
    ["op", "="],
    ["id", "c"],
    ["op", "*"],
    ["num", "5"],

    ["eol", 0],

    ["id", "print"],
    ["op", ":"],
    ["id", "c"],

    ["eol", 0]
]




"""

var = {
    "program": [
        {
            "type": "variable-declaration",
            "name": 0,
            "value": {
                "type": "literal-value",
                "value": 5
            }
        },
        {
            "type": "variable-declaration",
            "name": 1,
            "value": {
                "type": "literal-value",
                "value": 10
            }
        },
        {
            "type": "variable-declaration",
            "name": 2,
            "value": {
                "type": "binary-operation",
                "expression": "+",
                "a": {
                    "type": "variable-value",
                    "name": 0
                },
                "b": {
                    "type": "binary-operation",
                    "expression": "+",
                    "a": {
                        "type": "variable-value",
                        "name": 1
                    },
                    "b": {
                        "type": "literal-value",
                        "value": 1
                    }
                }
            }
        },
        {
            "type": "variable-affectation",
            "name": 2,
            "value": {
                "type": "binary-operation",
                "expression": "+",
                "a": {
                    "type": "literal-value",
                    "value": 5
                },
                "b": {
                    "type": "binary-operation",
                    "expression": "*",
                    "a": {
                        "type": "variable-value",
                        "name": 2
                    },
                    "b": {
                        "type": "literal-value",
                        "value": 5
                    }
                }
            }
        },
        {
            "type": "native-function",
            "name": "print",
            "parameters": [
                {
                    "type": "variable-value",
                    "name": 2
                }
            ]
        }
    ]
}

"""
#include <stdio.h>

int main()
{
    int a = 5;
    int b = 10;
    int c = a + b + 1;
    c = 5 + c * 5;
    printf("%i",c);
}
"""

"""
Errors

'<id><id>' : Unexcepted <id> fait
'<num><num>' : Unexcepted <num> fait
'<op><op>' : Unexcepted <op> fait
'<op.=>*<op.=>' : Unexcepted <op>
'<eol><eol>' : Unexcepted <eol> fait
'<op><eol>' : Incomplete expression fait
'*<id.native>' : Unexcepted fait 
'id.name.not-exist' fait 
'<id><num>'
'<num><id>'
"""

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


def scan(start, line):
    global varId
    global equalCount


    # print(start)
    # print(len(line))
    if start != len(line) - 1:
        currentEl = line[start]
        nextEl = line[start + 1]
        # print(currentEl)
        # print(NATIVES)
        # print(vartab)
        # print(currentEl)
        # print(isIdNative(currentEl))
        # check si pas 2 "="
        if currentEl.value == "=" :
            equalCount += 1
        if equalCount == 2: return "Error Syntax deux signes '="



        # en pimiere position NUM et OP interdit
        if (currentEl.type == TokenType.NUM or currentEl.type == TokenType.OP) and isBegin:
            return "Error Syntax: not a variable nor a native function"
        #  si la fonction native n'est pas en premiere place
        elif ((currentEl.type == TokenType.ID and isIdNative(currentEl) and start != 0) or
              (nextEl.type == TokenType.ID and isIdNative(nextEl) and start != 0)):
            return "Error Syntax: A native function must be in 1st position"
        #  si la fonction native est en première place elle DOIT etre suivi de :
        elif (currentEl.type == TokenType.ID and isIdNative(currentEl) and not nextEl.value ==":"):

            return "Error Syntax: A native function must be follow by ':'"

        # si la varible n'existe pas dans vartab et n'est pas en 1ere position
        elif currentEl.type == TokenType.ID and isIdNative(currentEl) == False and isVarNameAvailable(currentEl ,vartab)== False and start!= 0:

            return "Error Syntax: la varible '" + currentEl.value+"' n'est pas defini"

        # si la variable est en position 1 elle doit etre suivi d'un "=" (asignation ou delcaration)
        elif currentEl.type == TokenType.ID and not isIdNative(currentEl) and  nextEl.value != "=" and start ==0:
            return "Error Syntax: la varible '" + currentEl.value + "' n'est pas suivi d'un '='"


        # si la variable n'est PAS en position 1 elle DOIT etre suivi d' OP(not : ) ou  EOL)
        elif  not nextEl.value == ":" and currentEl.type == TokenType.ID  and not (nextEl.type == TokenType.OP or nextEl.type == TokenType.EOL ) and start != 0:
            return "Error Syntax: la varible '" + currentEl.value + "' est suivi d'un caractère incorect"


        # si le token est un un nombre , il DOIT etre suivis d' OP(not : et =) ou de EOL
        elif start == 0 and not nextEl.value == "=" and not nextEl.value == ":" and currentEl.type == TokenType.NUM and not (nextEl.type == TokenType.OP or nextEl.type == TokenType.EOL ):
            return "Error Syntax: le nombre '" + currentEl.value + "' est suivi d'un caractère incorect"

        #   si la variable est un operateur elle DOIT etre suvis d'une variable ou d'un nombre
        elif currentEl.type == TokenType.OP and not (nextEl.type == TokenType.ID or nextEl.type == TokenType.NUM ):
            return ("Error Syntax: l'operateur '" + currentEl.value + "' est suivi d'un caractère incorect")
        else:
            start += 1
            return scan(start, line)
    else:
        # si ligne ok

        # si declaration / on stocke dans vartab
        if isVarNameAvailable(line[0],vartab) == False and  isIdNative(line[0]) == False :

            varId+=1
            vartab[line[0].value] = varId



    return True


def parser(lines):
    global equalCount
    errortab = []
    for i in range(len(lines)):
        line = lines[i]
        equalCount = 0
        res = scan(0, line)
        if(res != True):
            errortab.append(res)
            print("Line "+ str(i+1) +": "+res)
        else:
            print(res)

    return errors
    # if not errors:
    #
    #
    #     print (lines)
    #     pass
    #
    #
    # else:
    #     print(errors)
