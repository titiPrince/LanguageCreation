from abc import ABC, abstractmethod


class TokenType:
    ID = "ID"
    OP = "OP"
    NUM = "NUM"
    EOL = "EOL"


class Token:
    def __init__(self, _type, _value):
        self.type = _type
        self.value = _value

    def __str__(self):
        return "TOKEN : Type = " + str(self.type) + " ; Value = " + str(self.value)


class Instruction(ABC):
    def toString(self, offset):
        indentation = " " * (4 * offset)
        inner = "    "
        newline = "\n" + indentation
        output = "{" + newline + inner + f'"type": {self.__class__.__name__}' + newline

        for key, value in self.__dict__.items():
            svalue = value
            if isinstance(value, Instruction):
                svalue = f"{value.toString(offset + 1)}"

            output += inner + f'"{key}": {svalue}' + newline

        output += "}"

        return output

    @abstractmethod
    def transpile(self):
        return ""


class LiteralNumber(Instruction):
    def __init__(self, value: int):
        self.value = value

    def transpile(self):
        return str(self.value)


class VarReading(Instruction):
    def __init__(self, name: str):
        self.name = name

    def transpile(self):
        return self.name


class BinaryOperation(Instruction):
    def __init__(self,
                 operator: str,
                 a: 'LiteralNumber | VarReading | BinaryOperation | None',
                 b: 'LiteralNumber | VarReading | BinaryOperation | None'):
        self.operator = operator
        self.a = a
        self.b = b

    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def transpile(self):
        return f"{self.a.transpile()}{self.operator}{self.b.transpile()}"


class VarAssignation(Instruction):
    def __init__(self, name: str, value: LiteralNumber | VarReading | BinaryOperation):
        self.name = name
        self.value = value

    def transpile(self):
        return f"{self.name}={self.value.transpile()};"


class VarDeclaration(Instruction):
    def __init__(self, name: str, value: LiteralNumber | VarReading | BinaryOperation):
        self.name = name
        self.value = value

    def transpile(self):
        return f"int {self.name}={self.value.transpile()};"


class NativeFunctionCall(Instruction):
    def __init__(self, name: str, *parameters: LiteralNumber | VarReading | BinaryOperation):
        self.name = name
        self.parameters = parameters

    def transpile(self):
        sparams = ""

        for param in self.parameters:
            sparams += param.transpile() + ","

        return f'{self.name}({sparams[0:-1]});'


class FunctionPrint(NativeFunctionCall):
    def __init__(self, *parameters: LiteralNumber | VarReading | BinaryOperation):
        super().__init__("printf", *parameters)

    def transpile(self):
        sparams = ""

        for param in self.parameters:
            sparams += param.transpile() + ","

        return f'{self.name}("%i\\n",{sparams[0:-1]});'



class AbstractSyntaxTree:
    def __init__(self, *instructions: Instruction):
        self.instructions = list(instructions)

    def __str__(self):
        output = '{\n    "program": [\n        '

        for instruction in self.instructions:
            output += instruction.toString(2) + ",\n        "

        return output[0:-10] + "\n    ]\n}"

    def addInstruction(self, *instructions: Instruction):
        self.instructions += instructions

    def transpile(self):
        output = "#include <stdio.h>\nint main(){"

        for instruction in self.instructions:
            output += instruction.transpile()

        return output + "}"


t = VarDeclaration("a", LiteralNumber(5))

# print(t.toString(0))
#
# f = BinaryOperation("-", LiteralNumber(1), LiteralNumber(1))
# h = BinaryOperation("+", f, LiteralNumber(9))
#
# q = FunctionPrint(h)
#
# g = AbstractSyntaxTree(t, q)
# # print(g.transpile())

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
