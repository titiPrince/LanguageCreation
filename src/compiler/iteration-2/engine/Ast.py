from .Symbols import *
from .Transpiler import *
from .VarManager import *


class Ast(AbstractSyntaxTree):
    def __init__(self, tokens: list[Token]):
        super().__init__(Block())

        self.tokens = tokens
        self.vm = VarManager()

        end, block = self.scanBlock(self.tokens)

        self.setBlock(block)


    def scanBasicInstruction(self, tokens: list[Token], end: str = Symbol.EOL) -> tuple[int, LiteralNumber | VarReading | BinaryOperation | VarAssignation]:
        lastParam = None
        currentParam = None

        for i, token in enumerate(tokens):
            # Instruction's end detection
            if token.value == end:
                return i + 1, lastParam

            # Token detection
            match token.type:
                case TokenType.ID:
                    if self.vm.exists(token.value):
                        varId = self.vm.getIdByName(token.value)
                        var = self.vm.getVarById(varId)

                        currentParam = VarReading(var)

                    else:
                        varId = self.vm.create(token.value)
                        var = self.vm.getVarById(varId)

                        currentParam = VarDeclaration(var)

                case TokenType.OP:
                    if token.value == Symbol.ASSIGN:
                        currentParam = VarAssignation()

                    elif token.value in Symbols.CALCULATIONS:
                        currentParam = BinaryOperation(token.value)

                case TokenType.NUM:
                    currentParam = LiteralNumber(token.value)

                case TokenType.STR:
                    currentParam = LiteralString(token.value)

            # Instruction assembler
            if lastParam is None:
                lastParam = currentParam

            elif isinstance(currentParam, VarAssignation):
                if isinstance(lastParam, VarDeclaration): continue

                currentParam.setVar(lastParam.variable)
                lastParam = currentParam

            elif isinstance(currentParam, (BinaryOperation, StringConcat)):
                if isinstance(lastParam, (VarAssignation, VarDeclaration)):
                    if isinstance(lastParam.value, (LiteralString, StringConcat)):
                        currentParam = StringConcat()

                    currentParam.setA(lastParam.value)
                    lastParam.setValue(currentParam)

                else:
                    if isinstance(lastParam, (LiteralString, StringConcat)):
                        currentParam = StringConcat()

                    currentParam.setA(lastParam)
                    lastParam = currentParam

            elif isinstance(currentParam, (LiteralNumber, LiteralString, VarReading)):
                if isinstance(lastParam, (VarAssignation, VarDeclaration)):
                    if lastParam.value is None:
                        lastParam.setValue(currentParam)

                        if isinstance(currentParam, LiteralNumber):
                            lastParam.var.setType(VarType.INTEGER)

                        elif isinstance(currentParam, LiteralString):
                            lastParam.var.setType(VarType.STRING)

                        else:
                            lastParam.var.setType(currentParam.variable.type)

                    elif isinstance(lastParam.value, (BinaryOperation, StringConcat)):
                        lastParam.value.setB(currentParam)
                else:
                    lastParam.setB(currentParam)


    def scanCondition(self, tokens: list[Token], end: str = Symbol.ACOS) -> tuple[int, Comparison]:
        print(">> Condition start <<")
        lastParam = None
        currentParam = None

        for i, token in enumerate(tokens):
            if token.value == end:
                print(">> Condition end <<", i)
                return i + 1, lastParam

            print(token)
            # Token detection
            match token.type:
                case TokenType.ID:
                    if token.value in (Symbol.AND, Symbol.NOT, Symbol.OR):
                        currentParam = BoolComparison(token.value)

                    else:
                        varId = self.vm.createOrGet(token.value)
                        var = self.vm.getVarById(varId)

                        currentParam = VarReading(var)

                case TokenType.OP:
                    if token.value in Symbol.CALCS:
                        currentParam = BinaryOperation(token.value)

                    else:
                        currentParam = Comparison(token.value)

                case TokenType.NUM:
                    currentParam = LiteralNumber(token.value)

                case TokenType.STR:
                    currentParam = LiteralString(token.value)

            # Condition assembler
            if lastParam is None:
                lastParam = currentParam

            elif isinstance(lastParam, (Comparison, BoolComparison)):
                if isinstance(currentParam, (Comparison, BoolComparison)):
                    currentParam.setA(lastParam)
                    lastParam = currentParam

                else:
                    lastParam.setB(currentParam)

            elif isinstance(currentParam, (Comparison, BoolComparison)):
                currentParam.setA(lastParam)
                lastParam = currentParam


    def scanIfStatement(self, tokens: list[Token]) -> tuple[int, IfStatement]:
        print(">> If start <<")
        # Main
        ptrCondition, condition = self.scanCondition(tokens)
        ptrBlock, block = self.scanBlock(tokens[ptrCondition:])
        print(f"ptrBlock: {ptrBlock}")

        statement = IfStatement(condition, block)

        pointer = ptrCondition + ptrBlock
        token = tokens[pointer]

        # Else if
        while token.value == Symbol.ELSEIF:
            ptrElseIfCondition, elseIfCondition = self.scanCondition(tokens[pointer + 1:])

            pointer += ptrElseIfCondition + 1
            ptrElseIfBlock, elseIfBlock = self.scanBlock(tokens[pointer:])

            pointer += ptrElseIfBlock

            statement.addElifBranch(ElseIfStatement(elseIfCondition, elseIfBlock))

            token = tokens[pointer]
            print("ICI NEXT", token)

        # Else
        if token.value == Symbol.ELSE:
            ptrElseBlock, elseBlock = self.scanBlock(tokens[pointer + 2:])

            statement.elseBranch = ElseStatement(elseBlock)

            pointer += ptrElseBlock + 2

        print(">> If end <<", pointer)
        return pointer, statement


    def scanForLoop(self, tokens: list[Token]) -> tuple[int, ForLoop]:
        print(">> For start <<")

        varId = self.vm.createOrGet(tokens[0].value)
        var = self.vm.getVarById(varId)

        self.vm.addVarToNextScope(var)

        ptrCondition, condition = self.scanCondition(tokens[2:], Symbol.FORSTEP)
        ptrIncr, incr = self.scanBasicInstruction(tokens[ptrCondition + 2:], Symbol.ACOS)
        ptrBlock, block = self.scanBlock(tokens[ptrCondition + 2 + ptrIncr:])

        statement = ForLoop(var, condition, incr, block)

        print(">> For end <<", ptrBlock)
        return ptrCondition + 2 + ptrIncr + ptrBlock, statement


    def scanFunctionParameters(self, tokens: list[Token]) -> tuple[
        int, list[LiteralNumber | LiteralString | VarReading | BinaryOperation]]:
        print(">> Function parameters start <<")
        parameters = []
        lastParam = None
        currentParam = None

        for i, token in enumerate(tokens):
            # Token detection
            match token.type:
                case TokenType.ID:
                    # Add here in the future, condition to verify if there is a function call

                    varId = self.vm.createOrGet(token.value)
                    var = self.vm.getVarById(varId)

                    currentParam = VarReading(var)

                case TokenType.NUM:
                    currentParam = LiteralNumber(token.value)

                case TokenType.STR:
                    currentParam = LiteralString(token.value)

                case TokenType.OP:
                    if token.value in Symbols.CONDITIONS:
                        currentParam = Comparison(token.value)

                    elif token.value in Symbol.CALCS:
                        currentParam = BinaryOperation(token.value)

                    elif token.value in Symbols.GATES:
                        currentParam = BoolComparison(token.value)

                case TokenType.BOX:
                    if token.value == Symbol.PARE:
                        parameters.append(lastParam)
                        print(">> Function parameters end <<", i)
                        return i + 2, parameters

                case TokenType.SEP:
                    currentParam = None

            # Condition assembler
            if lastParam is None:
                lastParam = currentParam

            elif currentParam is None:
                parameters.append(lastParam)
                lastParam = None

            elif isinstance(currentParam, (Comparison, BinaryOperation, BoolComparison)):
                currentParam.setA(lastParam)
                lastParam = currentParam

            elif isinstance(lastParam, (Comparison, BinaryOperation, BoolComparison)):
                lastParam.setB(currentParam)


    def scanBlock(self, tokens: list[Token]) -> tuple[int, Block]:
        print(">> Block start <<")

        self.vm.startScope()

        block = Block()

        skip = 0

        for i, token in enumerate(tokens):
            if skip > i:
                continue

            print(token)

            if token.value == Symbol.IF:
                skip, instruction = self.scanIfStatement(tokens[i + 1:])
                skip += 1

            elif token.value == Symbol.FOR:
                skip, instruction = self.scanForLoop(tokens[i + 1:])
                skip += 1

            elif token.value == Symbol.FCT_PRINT:
                skip, parameters = self.scanFunctionParameters(tokens[i + 2:])  # +2 to skip the (
                instruction = FunctionPrint(parameters)
                skip += 2

            elif token.value == Symbol.ACOE:
                print(">> Block end <<", i)

                self.vm.endScope()

                return i + 1, block

            else:
                skip, instruction = self.scanBasicInstruction(tokens[i:])
                print(f"Start: {i}, Skip: {skip}, End: {i + skip}\n")

            skip += i
            block.add(instruction)

        return len(tokens) - 1, block
