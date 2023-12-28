import importlib.util, sys
from src.compiler.iteration2.main import getOutputFromScript, getOutputFromFile


class UnitResult:
    def __init__(self, lexer: str = None, parser: str = None, ast: str = None, transpiler: str = None, execution: str = None):
        self.lexer = lexer
        self.parser = parser
        self.ast = ast
        self.transpiler = transpiler
        self.execution = execution

    def setLexer(self, lexer: str):
        self.lexer = lexer

    def setParser(self, parser: str):
        self.parser = parser

    def setAst(self, ast: str):
        self.ast = ast

    def setTranspiler(self, transpiler: str):
        self.transpiler = transpiler

    def setExecution(self, execution: str):
        self.execution = execution

    @staticmethod
    def fromFile(file_path: str) -> 'UnitResult':
        _types = ("", "", "", "", "")

        with open(file_path, 'r') as file:
            _lines = file.readlines()

            _state = 0
            _states = (
                '#LEXER',
                '#PARSER',
                '#AST',
                '#TRANSPILER',
                '#EXECUTION'
                ''
            )

            for _line in _lines:
                if _line == _states[_state]:
                    _state += 1
                    continue

                _types[_state - 1] += _line

        return UnitResult(_types[0], _types[1], _types[2], _types[3], _types[4])


class ScriptUnit:
    def __init__(self, script: str, result: UnitResult):
        self._script = script
        self._result = result

    def test(self) -> list[bool]:
        output = getOutputFromScript(self._script)

        return [
            output['tkn'] == self._result.lexer,
            output['err'] == self._result.parser,
            output['ast'] == self._result.ast,
            output['tsp'] == self._result.transpiler,
            output['exe'] == self._result.execution
        ]


class FileUnit(ScriptUnit):
    def __init__(self, file_path: str, result: UnitResult):
        file = open(file_path, 'r')
        script = file.read()
        file.close()

        super().__init__(script, result)


class UnitsTester:
    def __init__(self, compiler_path: str):
        pass
