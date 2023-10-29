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

'<id><id>' : Unexcepted <id>
'<num><num>' : Unexcepted <num>
'<op><op>' : Unexcepted <op>
'<op.=>*<op.=>' : Unexcepted <op>
'<eol><eol>' : Unexcepted <eol>
'<op><eol>' : Incomplete expression
'*<id.native>' : Unexcepted
"""

NATIVES = [
    "print"
]


def parser(tokens):
    vartab = {}
    print(tokens)
    lines = []
    line = []
    for i in range(len(tokens)-1):
        if tokens[i][0] != "eol":
            line.append((tokens[i][0], tokens[i][1]))
        else:
            line.append((tokens[i][0], tokens[i][1]))
            lines.append(line)
            line = []
    print(lines)
    for i in range(len(lines)):

        line = lines[i]
        # print(line)

        # print(line[1][0],line[1][1])
        # print(line[2][0],line[2][1])
            # print(j,len(line))
        if ( 1<len(line) and
             2 <len(line) and
             3 <len(line) and
             line[0][0] == "id" and
             line[0][0] not in NATIVES and
             line[1][1] == "=" and
             # line[2][1] in vartab a fix , ne check pas bien
             (line[2][0] == "num" or (line[2][0] == "id" and line[2][1] in vartab)) and
             line[3][1] == ";"):
            vartab[line[0][0]] = line[3][1]

            print("une déclaration simple ligne "+ str(i+1) )
            print("variable " +  line[0][1]+" initialisée")
            print("####################")

        elif ( 1<len(line) and
             2 <len(line) and
             3 <len(line) and
             line[0][0] == "id" and
             line[0][0] not in NATIVES and
             line[1][1] == "=" and
             (line[2][0] == "num" or (line[2][0] == "id" and line[2][1] in vartab)) and
             line[3][1] != ";"):

            start = 3
            next = 4
            last = 5

            # j'en suis la (verif si les deux prochains charac
            # sont operateur et nombre ou varibale deja déclarer
            # et si le 3eme est une fin de ligne , si non false,
            # si oui 2 charac mais pas fin de ligne continuer sinon finish)

            # while(start<len(line) and next < len(line) and last <len(line)):
            #     if(line[start][0] in "/*-+" and (line[next][0]== "num" or (line[2][0] == "num" or (line[2][0] == "id" and line[2][1] in NATIVES) )):
            #         start+=1
            #         next+=1
            #         last +=1
            #
            #     else:
            #         continue

            vartab[line[0][0]] = line[3][1]

            print("une declaration simple ligne "+ str(i+1) )
            print("variable " + line[0][1] + " initialisée")
            print("####################")


        else:
            print("ligne "+ str(i+1)+ "non valide")
            print("####################")
            # except IndexError:
            #     print("out of range")

            # Declaration simple




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
