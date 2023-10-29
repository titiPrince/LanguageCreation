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
            "value": 5
        },
        {
            "type": "variable-declaration",
            "name": 1,
            "value": 10
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
'id.name.not-exist'
"""

NATIVES = [
    "print"
]

vartab = {}
varId = 0


def isVarNameAvailable(element, vartab):
    return element.value in vartab.keys()


def isIdNative(element):
    return element.value in NATIVES


def scan(start, line):
    global varId

    equalsCount = 0
    # print(start)
    # print(len(line))
    if start != len(line) - 1:
        currentEl = line[start]
        nextEl = line[start + 1]
        # print(currentEl)
        # print(currentEl[0], nextEl[0])
        # print()

        # si deux element identiques a la suite
        if (currentEl.type == nextEl.type):
            return False

        # si op suivi de eol
        elif currentEl.type == TokenType.OP and nextEl.type == TokenType.EOL:
            return False
        #  si la fonction native n'est pas en premiere place
        elif ((currentEl.type == TokenType.ID and isIdNative(currentEl) and start != 0) or
              (nextEl.type == TokenType.ID and isIdNative(nextEl) and start != 0)):
            return False
        # si la varible n'existe pas
        elif currentEl.type == TokenType.ID and isIdNative(currentEl) == False and isVarNameAvailable(currentEl ,vartab)== False and start!= 0:
            return False
        else:
            start += 1
            return scan(start, line)
    else:
        # si ligne ok

        # si declaration
        if isVarNameAvailable(line[0],vartab) == False and  isIdNative(line[0]) == False):

            varId+=1
            vartab[line[0].value] = varId

            print(vartab)
        # sinon assination
        elif isVarNameAvailable(line[0],vartab) == True and  isIdNative(line[0] == False):
            # vartab[line[0].type]
            print(vartab)
        return True


def parser(lines):


    for i in range(len(lines)):
        line = lines[i]
        res = scan(0, line)
        print(res)

        # if name == "id":
        #     pass
        #
        # elif name == "op":
        #     pass
        #
        # elif name == "num":
        #     pass
        #
        # elif name == "eol":
        #     pass
        #
        # else:
        #     print("wtf whats happening: invalid token")
