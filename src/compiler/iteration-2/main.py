import sys, os
from time import time_ns

from engine.Lexer import *
# from engine import Parser
from engine.Transpiler import *
from engine.Ast import Ast

DEBUG = True

def nanoToMilli(nano: int) -> float:
    return nano / 1000000

start_total_time = time_ns()
if __name__ == '__main__':
    nargs = len(sys.argv)

    if nargs < 2:
        raise Exception("One argument is missing.")

    if nargs > 3:
        raise Exception("Too many arguments.")

    source = sys.argv[1]
    destination = source + ".o"

    if not os.path.exists(source):
        raise Exception("The source file doesn't exists.")

    if nargs == 3:
        destination = sys.argv[2]

    sourceFile = open(source, "r")

    script = sourceFile.read()

    sourceFile.close()

    if DEBUG: print("##################\n#### DEBUG ON ####\n##################")

    start_lexer_time = time_ns()
    tokens = lexer(script)
    lexer_time = time_ns() - start_lexer_time

    start_parser_time = time_ns()
    # errors = Parser.scan(tokens)
    parser_time = time_ns() - start_parser_time
    # print(errors)

    if not False: # si pas d'erreurs venant du parser

        start_ast_time = time_ns()
        ast = Ast(tokens)
        ast_time = time_ns() - start_ast_time

        start_transpiler_time = time_ns()
        transpiled = ast.transpile()
        transpiler_time = time_ns() - start_transpiler_time

        destFile = open(source + ".c", "w")
        destFile.write(transpiled)
        destFile.close()

        start_compiler_time = time_ns()
        os.system("gcc " + source + ".c -o " + destination)
        compiler_time = time_ns() - start_compiler_time


        if DEBUG:
            print("\n################\n#### RESULT ####\n################")

        else:
            os.remove(source + ".c")
            os.system("clear")

        start_execution_time = time_ns()
        os.system("./" + destination)
        execution_time = time_ns() - start_execution_time

        total_time = time_ns() - start_total_time

        if DEBUG:
            print("\n#####################\n#### PERFORMANCE ####\n#####################")
            print(f"LEXER:\t\t{nanoToMilli(lexer_time)} ms")
            print(f"PARSER:\t\t{nanoToMilli(parser_time)} ms")
            print(f"AST:\t\t{nanoToMilli(ast_time)} ms")
            print(f"TRANSPILER:\t{nanoToMilli(transpiler_time)} ms")
            print(f"COMPILER:\t{nanoToMilli(compiler_time)} ms")
            print(f"EXECUTION:\t{nanoToMilli(execution_time)} ms")
            print(f"OTHER:\t\t{nanoToMilli(total_time - lexer_time - parser_time - ast_time - transpiler_time - compiler_time - execution_time)} ms")
            print("-------------------------")
            print(f"TOTAL:\t\t{nanoToMilli(total_time)} ms")

    else:
        raise Exception("\n".join(errors))
