from engine.tester import *

variables = ScriptUnit(
    "Variables",
    'a=5;print(a);b=a*5;print(b);c=b*5;print(c);',
    UnitResult()
)


if __name__ == '__main__':
    print("Tests started!")
    print(variables.test())