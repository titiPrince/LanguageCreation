## Syntaxe du Langage

### Commentaires

Les commentaires sont créés en utilisant `//` suivi du texte du commentaire.

```plaintext
// Ceci est un commentaire
```

### Déclaration de Variable

La déclaration d'une variable se fait en utilisant le signe égal (`=`) suivi de la valeur initiale.

```plaintext
a = 0;
```

### Affectation de Variable

Pour affecter une nouvelle valeur à une variable existante, utilisez également le signe égal (`=`).

```plaintext
a = 0;
```

### Conditions

Les conditions sont définies avec les mots-clés `si`, `et si`, et `sinon`. Le code conditionnel est encapsulé par des accolades `{}`.

```plaintext
si condition {
    // Code à exécuter si la condition est vraie
}
et si condition {
    // Code à exécuter si la condition est vraie
}
sinon {
    // Code à exécuter si aucune condition précédente n'est vraie
}
```

### Boucle "for"

Une boucle "for" est créée avec le mot-clé `pour`. Elle inclut une variable d'itération, une condition, et une expression d'incrémentation.

```plaintext
pour i quand i < 5 tous i++ {
    // Code à répéter tant que la condition est vraie
}
```

### Boucle "while"

Une boucle "while" est créée avec le mot-clé `tant que`. Elle inclut une condition.

```plaintext
tant que condition {
    // Code à répéter tant que la condition est vraie
}
```

### Déclaration de Fonction

Les fonctions sont déclarées avec le mot-clé `proc`. Les paramètres de la fonction sont énumérés entre parenthèses `()`.

```plaintext
proc nom param1 param2 param3 {
    // Corps de la fonction

    return param1;
}
```

### Appel de Fonction

Pour appeler une fonction, utilisez son nom suivi des arguments entre parenthèses.

```plaintext
aFunction(0, 1, 3);
aFunction(0, anotherFunction(0), 5);
```

Cette syntaxe rend le langage facile à lire et à écrire, tout en permettant des fonctionnalités avancées de programmation.