input = 7;

si input >= 0 et input < 20 {
  fact = 1;

  i = 1;
  pour i quand i <= input incr 1 {
    fact = fact * i;
  }

  print("Le factorielle de", input, "est", fact);
}
sinon {
  print("L'input doit etre positif");
  print("L'input ne peux pas etre superieur a 19 car sa depasse la valeur max de int");
}