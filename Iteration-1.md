# Objectifs
Créer un langage très simple basé uniquement sur des calculs mathématiques, des variables et une fonction permettant d'afficher un nombre.

# Features
- Operations mathematique `+ - * /`
- Assignation de variables `nomdevariable = 0`
- Affichage `print nomdevariable`

# Fonctionnement
Le compiler est fait en Python et transpile vers du **C** puis compile en langage machine et l'execute.
- Lexer
- Parser error handler
- Parser Abstract syntax tree
- Transpiler
- GCC