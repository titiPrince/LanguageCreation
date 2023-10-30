# Comment ca marche ?
Un langage de programmation fonctionne a l'image des langues comme le Francais ou l'Anglais, au fond ce n'est qu'une suite de caracteres et de nombre auquels on donne du sens selon leur agencement.
Le Francais et l'Anglais bien que partageant le meme alphabet vont etre interpreter differement comme par exemple Python et Javascript.

## Les differentes etapes

### Prerequis : Un fichier texte
Pour fonctionner notre langage auras besoin d'un fichier texte (tous les langages de programmation ne font que lire des fichiers texte selon leur propre regles).   

Un exemple simple :
```
print: 42 * var + 1
``` 


### Etape 1 : **Lexer** _(Analyseur lexical)_
Le **lexer** est un programme qui va segmenter le fichier texte, et trier ce qu'il si trouve dans une liste clef valeurs.

![image](https://github.com/titiPrince/LanguageCreation/assets/53018497/a62cb28c-43ca-48ff-a6e6-24b08415c32e)

   
### Etape 2 : **Parser** _(Analyseur syntaxique)_
Le **parser** est un autre programme qui lui va prendre le resultat du **lexer** et structurer et verifier les instructions.

### Etape 3 : **Transpiler**
Le Transpiler utilise le json generer par le parser et se charge de le traduire en un langage de programmation qui sera lui meme transpiler a son tours jusqu'a etre compile en code machine.
