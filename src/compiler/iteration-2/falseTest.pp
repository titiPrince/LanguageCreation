chaine = "Ceci est une chaine de caractere";
autrechaine = "un exemple" + chaine + "test" + " waw";

a = "a";
b = "b" + a + "test";

c = 1 + 2 * 5;

si b == "ba" {
  a = "ab";
}
sinon
{
  a = "aba";
}

si 0 { print("c'est 0"); }
etsi a == "ba" et 1 != 1 ou 1 > 5 {
  print("c'est 1");
}
sinon {
  print("c'est rien");
}

count = 0;

pour c quand c<50 incr 4 {
  print(c);
  count = count + 1;
}

a = "fin du fichier";
