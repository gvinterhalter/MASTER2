



is_a(a, b).
is_a(c, b).
is_a(b, d).
is_a(f, e).
is_a(e, g).
is_a(g, d).


is_a(e, a).
is_a(e, d).


is_a*(A, B) :- is_a(A, B).
is_a*(A, C) :- is_a(A, B), is_a*(B, C).


