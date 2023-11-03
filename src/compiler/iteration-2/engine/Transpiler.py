from abc import ABC, abstractmethod


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


class LiteralString(Instruction):
    def __init__(self, value: str):
        self.value = value

    def transpile(self):
        return '"self.value"'


class VarReading(Instruction):
    def __init__(self, name: str):
        self.name = name

    def transpile(self):
        return self.name


class BinaryOperation(Instruction):
    def __init__(self,
                 operation: str,
                 a: 'LiteralNumber | VarReading | BinaryOperation | None' = None,
                 b: 'LiteralNumber | VarReading | BinaryOperation | None' = None):
        self.operation = operation
        self.a = a
        self.b = b

    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def transpile(self):
        return f"{self.a.transpile()}{self.operation}{self.b.transpile()}"


class StringConcat(Instruction):
    def __init__(self,
                 a: 'LiteralString | VarReading | StringConcat | None' = None,
                 b: 'LiteralString | VarReading | StringConcat | None' = None):
        self.a = a
        self.b = b

    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def transpile(self): # MARCHE PAS CAR `a` PEUT ETRE LiteralString ET DONC STRCAT MARCHE PAS
        return f"strcat({self.a.transpile()},{self.b.transpile()});"


class Condition(Instruction):
    def __init__(self,
                 operator: str,
                 a: 'LiteralNumber | LiteralString | VarReading | BinaryOperation | Condition | None',
                 b: 'LiteralNumber | LiteralString | VarReading | BinaryOperation | Condition | None'):
        self.operator = operator
        self.a = a
        self.b = b

    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def transpile(self):
        return f"{self.a.transpile()}{self.operator}{self.b.transpile()}"


class Block(Instruction):
    def __init__(self, *instructions: Instruction):
        self.instructions = [*instructions]

    def add(self, *instructions: Instruction):
        self.instructions += [*instructions]


class ElseStatement(Instruction):
    def __init__(self, block: Block):
        self.block = block


class ElseIfStatement(Instruction):
    def __init__(self,
                 condition: Condition,
                 block: Block):
        self.condition = condition
        self.block = block


class IfStatement(Instruction):
    def __init__(self,
                 condition: Condition,
                 block: Block,
                 branch: list[Instruction] | None):
        self.condition = condition
        self.block = block
        self.branch = branch

    def addBranch(self, *branch):
        self.branch = [*branch]


class ForLoop(Instruction): pass


class VarAssignation(Instruction):
    def __init__(self, name: str, value: LiteralNumber | VarReading | BinaryOperation = None):
        self.name = name
        self.value = value

    def setValue(self, value: LiteralNumber | VarReading | BinaryOperation):
        self.value = value

    def transpile(self):
        return f"{self.name}={self.value.transpile()};"


class VarDeclaration(Instruction):
    def __init__(self, name: str, value: LiteralNumber | LiteralString | VarReading | BinaryOperation = None):
        self.name = name
        self.value = value

    def transpile(self):
        if isinstance(self.value, LiteralString):
            return f"char {self.name}[]={self.value.transpile()};"

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
        output = "#include <stdio.h>\n#include <string.h>\nint main(){"

        for instruction in self.instructions:
            output += instruction.transpile()

        return output + "}"


t = VarDeclaration("a", LiteralNumber(5))
