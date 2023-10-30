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


def transpile(lines):
    for line in lines:
        line.reverse()

        prevToken = None
        skipNext = False

        for i, token in enumerate(line):
            # if token.value == Symbol.ASSIGN: break
            if token.type == TokenType.EOL: continue

            if token.type == TokenType.NUM:
                if isinstance(prevToken, BinaryOperation):
                    # dcp faire d'autre trucks
                prevToken = LiteralNumber(token.value)

            elif token.type == TokenType.ID:
                prevToken = VarReading(token.value)

            elif token.type == TokenType.OP:
                if token.value in Symbol.OPERATIONS:
                    prevToken = BinaryOperation(token.value, None, prevToken)

                # IL MANQUE LE FAIT QUE LE BINARY OPERATION PRECEDENT NE SOIT PAS REFILER DANS L'OPERATION SUIVANTE

                print(lastOperation)


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
