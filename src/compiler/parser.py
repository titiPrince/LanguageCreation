"""
[
    ["id", "a"],
    ["op", "="],
    ["num", "5"],

    ["id", "b"],
    ["op", "="],
    ["num", "10"],

    ["id", "c"],
    ["op", "="],
    ["id", "a"],
    ["op", "+"],
    ["id", "b"],
    ["op", "+"],
    ["num", "1"]

    ["id", "c"],
    ["op", "="],
    ["id", "c"],
    ["op", "*"],
    ["num", "5"],

    ["id", "print"],
    ["op", ":"],
    ["id", "c"]
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

"""



def parser(tokens):
    for token in tokens:
        pass
