from classes import *


class Symbol:
    ASSIGN = "="
    EQUAL = "=="
    CALL = ":"
    EOL = ";"
    MUL = "*"
    ADD = "+"
    SUB = "-"
    DIV = "/"
    OPERATIONS = "+-*/"


vartab = {}
varincr = 0


def varDeclared(var):
    return var in vartab.keys()


def transpile(lines):
    global varincr

    ast = AbstractSyntaxTree()

    for line in lines:
        line.reverse()

        prevInstruct = None
        currentInstr = None

        for i, token in enumerate(line):
            # if token.value == Symbol.ASSIGN: break
            if token.type == TokenType.EOL: continue

            if token.type == TokenType.NUM:
                currentInstr = LiteralNumber(token.value)

            elif token.type == TokenType.ID:
                currentInstr = VarReading(token.value)

            elif token.type == TokenType.OP:
                if token.value in Symbol.OPERATIONS:
                    currentInstr = BinaryOperation(token.value, None, prevInstruct)

                elif token.value == Symbol.ASSIGN:
                    nextToken = line[i+1]

                    if varDeclared(nextToken.value):
                        currentInstr = VarAssignation(nextToken.value, prevInstruct)

                    else:
                        currentInstr = VarDeclaration(nextToken.value, prevInstruct)
                        vartab[nextToken.value] = varincr
                        varincr += 1

                    ast.addInstruction(currentInstr)
                    break

                elif token.value == Symbol.CALL:
                    ast.addInstruction(FunctionPrint(prevInstruct))
                    break

            if isinstance(prevInstruct, BinaryOperation):
                if not isinstance(currentInstr, BinaryOperation):
                    prevInstruct.setA(currentInstr)
                else:
                    prevInstruct = currentInstr

            else:
                prevInstruct = currentInstr

    return ast.transpile()


def transpile2(lines):
    for line in lines:
        line.reverse()
        for i, currentToken in enumerate(line):
            # if token.value == Symbol.ASSIGN: break
            if token.type != TokenType.OP: continue

            prevToken = line[i - 1]
            nextToken = line[i + 1]
            curentToken = line[i]
            lastOperation = ""

            if token.value in Symbol.OPERATIONS:
                print(prevToken)

                if lastOperation == "" and curentToken.value == "=":

                    if curentToken.type == TokenType.NUM:
                        a = LiteralNumber(curentToken.value)
                    else:
                        a = VarReading(curentToken.value)

                if lastOperation == "":
                    if prevToken.type == TokenType.NUM:
                        a = LiteralNumber(prevToken.value)
                    else:
                        a = VarReading(prevToken.value)

                    if nextToken.type == TokenType.NUM:
                        b = LiteralNumber(nextToken.value)
                    else:
                        b = VarReading(nextToken.value)
                    lastOperation = (BinaryOperation(token.value, b, a).toString(0))


                else:
                    if line[i].value == "=":
                        t = VarDeclaration(line[i + 2].value, VarReading(lastOperation))
                        q = FunctionPrint(t)

                        g = AbstractSyntaxTree(t, q)
                        print(g.transpile())

                    if nextToken.type == TokenType.NUM:
                        b = LiteralNumber(nextToken.value)
                    else:
                        b = VarReading(nextToken.value)

                # IL MANQUE LE FAIT QUE LE BINARY OPERATION PRECEDENT NE SOIT PAS REFILER DANS L'OPERATION SUIVANTE

                print(lastOperation)
