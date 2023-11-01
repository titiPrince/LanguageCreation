cha1ne = "Ceci est une chaine de caractere";
autrechaine = "un exemple" + chaine + "test" + " waw";

a = "a";
b = "b" + a;

si b == "ba" {
  a = "ab";
}
sinon
{
  a = "aba";
}

si 0 {
  print("c'est 0");
}
etsi 1 {
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