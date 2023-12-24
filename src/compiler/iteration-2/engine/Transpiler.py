from abc import ABC, abstractmethod
from .VarManager import *


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

            elif isinstance(value, list):
                svalue = f"[{newline+inner*2}{f',{newline+inner*2}'.join([i.toString(offset+2)for i in value])}{newline+inner}]"

            output += inner + f'"{key}": {svalue}' + newline

        output += "}"

        return output

    @abstractmethod
    def transpile(self) -> str:
        return ""


class LiteralNumber(Instruction):
    def __init__(self, value: int):
        self.value = value

    def transpile(self) -> str:
        return str(self.value)


class LiteralString(Instruction):
    def __init__(self, value: str):
        self.value = value

    def transpile(self) -> str:
        return f'"{self.value}"'


class VarReading(Instruction):
    def __init__(self, name: str):
        self.name = name

    def transpile(self) -> str:
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

    def transpile(self) -> str:
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

    def transpile(self) -> str:
        return f"C1({self.a.transpile()},{self.b.transpile()})"


class Comparison(Instruction):
    def __init__(self,
                 comparator: str,
                 a: 'LiteralNumber | LiteralString | VarReading | BinaryOperation | Condition | None' = None,
                 b: 'LiteralNumber | LiteralString | VarReading | BinaryOperation | Condition | None' = None):
        self.comparator = comparator
        self.a = a
        self.b = b

    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def transpile(self) -> str:
        return f"{self.a.transpile()}{self.comparator}{self.b.transpile()}"


class BoolComparison(Instruction):
    def __init__(self,
                 comparator: str,
                 a: 'Condition | None' = None,
                 b: 'Condition | None' = None):
        self.comparator = comparator
        self.a = a
        self.b = b

    def setA(self, a: Comparison):
        self.a = a

    def setB(self, b: Comparison):
        self.b = b

    def transpile(self) -> str:
        return f"{self.a.transpile()}{self.comparator}{self.b.transpile()}"


class Block(Instruction):
    def __init__(self):
        self.instructions: list[Instruction] = []

    def add(self, instruction: Instruction):
        self.instructions.append(instruction)

    def transpile(self) -> str:
        return "".join([i.transpile() for i in self.instructions])


class ElseStatement(Instruction):
    def __init__(self, block: Block):
        self.block = block

    def transpile(self) -> str:
        return f"else{{{self.block.transpile()}}}"


class ElseIfStatement(Instruction):
    def __init__(self,
                 condition: Comparison,
                 block: Block):
        self.condition = condition
        self.block = block

    def transpile(self) -> str:
        return f"else if({self.condition.transpile()}){{{self.block.transpile()}}}"


class IfStatement(Instruction):
    def __init__(self,
                 condition: Comparison,
                 block: Block,
                 elifBranch: list[ElseIfStatement] = [],
                 elseBranch: ElseStatement = None):
        self.condition = condition
        self.block = block
        self.elifBranch = elifBranch
        self.elseBranch = elseBranch

    def addElifBranch(self, branch):
        self.elifBranch.append(branch)

    def setElseBranch(self, branch):
        self.elseBranch = branch

    def transpile(self) -> str:
        elifs = "".join([b.transpile() for b in self.elifBranch]) if self.elifBranch else ""
        return f"if({self.condition.transpile()}){{{self.block.transpile()}}}{elifs}{self.elseBranch.transpile()}"


class VarAssignation(Instruction):
    def __init__(self, name: str | None = None, value: LiteralNumber | LiteralString | VarReading | BinaryOperation | StringConcat = None):
        self.name = name
        self.value = value

    def setName(self, name: str):
        self.name = name

    def setValue(self, value: LiteralNumber | LiteralString | VarReading | BinaryOperation | StringConcat):
        self.value = value

    def transpile(self) -> str:
        if isinstance(self.value, (LiteralString, StringConcat)):
            return f"SS1(&{self.name},{self.value.transpile()});"
        return f"{self.name}={self.value.transpile()};"


class ForLoop(Instruction):
    def __init__(self,
                 var: str,
                 condition: Comparison,
                 incr: LiteralNumber | VarReading | BinaryOperation | VarAssignation = None,
                 block: Block = None):
        self.var = var
        self.condition = condition
        self.incr = incr
        self.block = block

    def transpile(self) -> str:
        if isinstance(self.incr, VarAssignation):
            _incr = f"{self.incr.transpile()}"

        elif isinstance(self.incr, LiteralNumber):
            _incr = f"{self.var}={self.var}+({self.incr.transpile()})"

        else:
            _incr = f"{self.var}={self.incr.transpile()}"

        return (f"for(int {self.var}=0;{self.condition.transpile()};{_incr})"
                f"{{{self.block.transpile()}}}")


class VarDeclaration(Instruction):
    def __init__(self, name: str = None, value: LiteralNumber | LiteralString | StringConcat | VarReading | BinaryOperation = None):
        self.name = name
        self.value = value

    def setName(self, name: str):
        self.name = name

    def setValue(self, value: LiteralNumber | LiteralString | VarReading | BinaryOperation | StringConcat):
        self.value = value

    def transpile(self) -> str:
        if isinstance(self.value, (LiteralString, StringConcat)):
            return f"char* {self.name}={self.value.transpile()};"

        return f"int {self.name}={self.value.transpile()};"


class NativeFunctionCall(Instruction):
    def __init__(self, name: str, parameters: list[LiteralNumber | VarReading | BinaryOperation]):
        self.name = name
        self.parameters = parameters

    def transpile(self) -> str:
        sparams = ""

        for param in self.parameters:
            sparams += param.transpile() + ","

        return f'{self.name}({sparams[0:-1]});'


class FunctionPrint(NativeFunctionCall):
    def __init__(self, parameters: list[LiteralNumber | LiteralString | VarReading | BinaryOperation]):
        super().__init__("printf", parameters)

    def transpile(self) -> str:
        sparams = ""

        for param in self.parameters:
            sparams += param.transpile() + ","

        return f'{self.name}("%i\\n",{sparams[0:-1]});'


class AbstractSyntaxTree:
    def __init__(self, block: Block | None = None):
        self.block: Block | None = block
        self.instructions = list(block.instructions)

    def __str__(self):
        output = '{\n    "program": [\n        '

        for instruction in self.instructions:
            output += instruction.toString(2) + ",\n        "

        return output[0:-10] + "\n    ]\n}"

    def setBlock(self, block: Block):
        self.block: Block | None = block
        self.instructions = list(block.instructions)

    def addInstruction(self, *instructions: Instruction):
        print("INSTRUCTION", instructions)
        self.instructions += instructions

    def transpile(self) -> str:
        output = ("#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\n"
                  "char* C1(const char* str1,const char* str2){size_t len1=strlen(str1);size_t len2=strlen("
                  "str2);char* result=(char*)malloc(len1+len2+1);if(result==NULL)return NULL;memcpy(result,str1,"
                  "len1);memcpy(result+len1,str2,len2+1);return result;}\n"
                  "void SS1(char** dest,const char* src){size_t length=strlen(src);"
                  "*dest=(char*)malloc((length+1)*sizeof(char));if(*dest!=NULL){strcpy(*dest, src);}}\n"
                  "int main(){\n")

        for instruction in self.instructions:
            output += instruction.transpile()

        return output + "}"


if __name__ == '__main__':
    root = AbstractSyntaxTree(
        VarDeclaration("cha1ne", LiteralString("Ceci est une chaine de caractere")),
        VarDeclaration("autrechaine",
                       StringConcat(
                           LiteralString("un exemple"),
                           StringConcat(
                               VarReading("cha1ne"),
                               StringConcat(
                                   LiteralString("test"),
                                   LiteralString("waw")
                               )
                           )
                       )),
        VarDeclaration("a", LiteralString("a")),
        VarDeclaration("b",
                       StringConcat(
                           LiteralString("b"),
                           StringConcat(
                               VarReading("a"),
                               LiteralString("test")
                           )
                       )),
        VarDeclaration("c",
                       BinaryOperation("+",
                                       LiteralNumber(1),
                                       BinaryOperation("*",
                                                       LiteralNumber(2),
                                                       LiteralNumber(5)
                                                       )
                                       )
                       ),
        IfStatement(
            Comparison("==",
                       VarReading("b"),
                       LiteralString("ba")
                       ),
            Block(
                VarAssignation("a",
                               LiteralString("ab")
                               )
            ), None,
            ElseStatement(
                Block(
                    VarAssignation("a",
                                   LiteralString("aba")
                                   )
                )
            )
        ),
        IfStatement(
            Comparison("!=",
                       LiteralNumber(0),
                       LiteralNumber(0)
                       ),
            Block(
                FunctionPrint(
                    LiteralString("C'est 0")
                )
            ),
            [
                ElseIfStatement(
                    Comparison(
                        "==",
                        VarReading("a"),
                        Comparison(
                            "and",
                            LiteralString("ba"),
                            Comparison(
                                "!=",
                                LiteralNumber(1),
                                Comparison(
                                    "or",
                                    LiteralNumber(1),
                                    Comparison(
                                        ">",
                                        LiteralNumber(1),
                                        LiteralNumber(5)
                                    )
                                )
                            )
                        )
                    ),
                    Block(
                        FunctionPrint(LiteralString("C'est 1"))
                    )
                )
            ],
            ElseStatement(
                Block(
                    FunctionPrint(LiteralString("C'est rien"))
                )
            )
        ),
        VarDeclaration("count", LiteralNumber(0)),
        ForLoop(
            "i",
            Comparison(
                "<",
                VarReading("i"),
                LiteralNumber(50)
            ),
            LiteralNumber(1),
            Block(
                FunctionPrint(VarReading("count")),
                VarAssignation(
                    "count",
                    BinaryOperation(
                        "+",
                        VarReading("count"),
                        LiteralNumber(1)
                    )
                )
            )
        )
    )

    print(root.transpile())
