cha1ne = "Ceci est une chaine de caractere";
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
etsi a == "ba" and 1 != 1 or 1 > 5 {
  print("c'est 1");
}
sinon {
  print("c'est rien");
}

count = 0;

pour i quand i<50 incr 1 {
  print(count);
  count = count + 1;
}
