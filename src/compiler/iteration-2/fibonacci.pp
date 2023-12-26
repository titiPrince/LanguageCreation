max = 20;

n1 = 0;
n2 = 1;

next = 0;

pour i quand i < max incr 1 {
  si i <= 1 {
    next = i;
  }
  sinon {
    next = n1 + n2;
    n1 = n2;
    n2 = next;
  }

  print(next);
}