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
    vars = {}

    for token in tokens:
        name = token[0]
        value = token[1]

        # Declaration simple
        if name == "id":
            pass

        elif name == "op":
            pass

        elif name == "num":
            pass

        elif name == "eol":
            pass

        else:
            print("wtf whats happening: invalid token")
