from .Symbols import *
from .Transpiler import *
from .VarManager import *


def scanInstruction(tokens: list[Token]) -> tuple[int, LiteralNumber | VarReading | BinaryOperation | VarAssignation]:
    lastParam = None
    currentParam = None

    skip = 0

    for i, token in enumerate(tokens):
        # Token detection
        match token.type:
            case TokenType.ID:
                currentParam = VarReading(token.value)

            case TokenType.OP:
                if token.value == Symbol.ASSIGN:
                    currentParam = VarAssignation()

            case TokenType.NUM:
                break

            case TokenType.STR:
                break

            case TokenType.BOX:
                break

            case TokenType.SEP:
                break

        # Instruction assembler
        if lastParam is None:
            lastParam = currentParam

        elif isinstance(currentParam, VarAssignation):
            currentParam.setName(lastParam.name)
            lastParam = currentParam


def scanCondition(tokens: list[Token]) -> tuple[int, Condition]:
    lastParam = None
    currentParam = None

    for i, token in enumerate(tokens):
        # Token detection
        match token.type:
            case TokenType.ID:
                if token.value in (Symbol.AND, Symbol.NOT, Symbol.OR):
                    currentParam = BoolComparison(token.value)

                else:
                    currentParam = VarReading(token.value)

            case TokenType.OP:
                if token.value in Symbol.CALCS:
                    currentParam = BinaryOperation(token.value)

                else:
                    currentParam = Condition(token.value)

            case TokenType.NUM:
                currentParam = LiteralNumber(token.value)

            case TokenType.STR:
                currentParam = LiteralString(token.value)

            case TokenType.BOX:
                if token.value == Symbol.ACOS:
                    return i, lastParam

        # Condition assembler
        if lastParam is None:
            lastParam = currentParam

        elif isinstance(lastParam, (Condition, BoolComparison)):
            lastParam.setB(currentParam)

        elif isinstance(currentParam, (Condition, BoolComparison)):
            currentParam.setA(lastParam)
            lastParam = currentParam


def scanIfStatement(tokens: list[Token]) -> tuple[int, IfStatement]:
    # Main
    ptrCondition, condition = scanCondition(tokens)
    ptrBlock, block = scanBlock(tokens[ptrCondition + 1:])

    statement = IfStatement(condition, block)

    token = tokens[ptrBlock + 1]
    pointer = ptrBlock + 1

    # Else if
    while token.value == Symbol.ELSEIF:
        ptrElseIfCondition, elseIfCondition = scanCondition(tokens[pointer + 1:])
        ptrElseIfBlock, elseIfBlock = scanBlock(tokens[ptrElseIfCondition + 1:])

        statement.addElifBranch(ElseIfStatement(elseIfCondition, elseIfBlock))

        token = tokens[ptrElseIfBlock + 1]
        pointer = ptrElseIfBlock + 1

    # Else
    if token == Symbol.ELSE:
        ptrElseBlock, elseBlock = scanBlock(tokens[pointer + 1:])

        statement.elseBranch = ElseStatement(elseBlock)

        pointer = ptrElseBlock + 1

    return pointer, statement


def scanForLoop(tokens: list[Token]) -> tuple[int, ForLoop]:
    var = tokens[0].value

    ptrCondition, condition = scanCondition(tokens[1:])
    ptrIncr, incr = scanInstruction(tokens[ptrCondition + 2:])
    ptrBlock, block = scanBlock(tokens[ptrIncr + 1:])

    statement = ForLoop(var, condition, incr, block)

    return ptrBlock, statement


def scanFunctionParameters(tokens: list[Token]) -> tuple[
    int, list[LiteralNumber | LiteralString | VarReading | BinaryOperation]]:
    parameters = []
    lastParam = None
    currentParam = None

    for i, token in enumerate(tokens):
        # Token detection
        match token.type:
            case TokenType.ID:
                # Add here in the future, condition to verify if there is a function call

                currentParam = VarReading(token.value)

            case TokenType.NUM:
                currentParam = LiteralNumber(token.value)

            case TokenType.STR:
                currentParam = LiteralString(token.value)

            case TokenType.OP:
                if token.value in Symbols.CONDITIONS:
                    currentParam = Condition(token.value)

                elif token.value in Symbol.CALCS:
                    currentParam = BinaryOperation(token.value)

                elif token.value in Symbols.GATES:
                    currentParam = BoolComparison(token.value)

            case TokenType.BOX:
                if token.value == Symbol.PARE:
                    parameters.append(lastParam)

                    return i, parameters

            case TokenType.SEP:
                currentParam = None

        # Condition assembler
        if lastParam is None:
            lastParam = currentParam

        elif currentParam is None:
            parameters.append(lastParam)
            lastParam = None

        elif isinstance(currentParam, (Condition, BinaryOperation, BoolComparison)):
            currentParam.setA(lastParam)
            lastParam = currentParam

        elif isinstance(lastParam, (Condition, BinaryOperation, BoolComparison)):
            lastParam.setB(currentParam)


def scanBlock(tokens: list[Token]) -> tuple[int, Block]:
    block = Block()

    skip = 0

    for i, token in enumerate(tokens):
        if skip:
            skip -= 1
            continue

        if token.value == Symbol.IF:
            skip, instruction = scanIfStatement(tokens[i + 1:])

        elif token.value == Symbol.FOR:
            skip, instruction = scanForLoop(tokens[i + 1:])

        elif token.value == Symbol.FCT_PRINT:
            skip, instruction = scanFunctionParameters(tokens[i + 2:])  # +2 to skip the (

        elif token.value == Symbol.ACOE:
            return i, block

        block.add(instruction)


def getAbstractTree(tokens: list[Token]) -> AbstractSyntaxTree:
    ast = AbstractSyntaxTree()

    for i, token in enumerate(tokens):
        match token.type:
            case TokenType.ID:
                break

            case TokenType.OP:
                break

            case TokenType.NUM:
                break

            case TokenType.STR:
                break

            case TokenType.BOX:
                break

            case TokenType.SEP:
                stackInstruction = []

    return ast
