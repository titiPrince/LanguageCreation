cha1ne = "Ceci est une chaine de caractere";
autrechaine = "un exemple" + chaine + "test" + " waw";
si i = 2 {;
  si i = 2 { "2"};
a = "a";
b = "b" + a;

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

pour i quand i<50 incr i++ {
  print(count);
  count = count + 1;
}
