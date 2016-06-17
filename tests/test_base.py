# tests

assert List[1, 2, 3] + (4, 5, 6) == List[1, 2, 3, 4, 5, 6]
assert List[1, 2, 3].Tuple() == Tuple[1, 2, 3]
assert List[1, 2, 3].map(str).Tuple() == Tuple["1", "2", "3"]
assert List[1, 2, 3].apply(lambda *args: sum(args)) == 6
assert List[1, 2, 3].reduce(0, (lambda res, x: res + x)) == 6
assert List[1, 2, 3].reduce((), (lambda res, x: res + (x, ))) == (1, 2, 3)

assert str(List[1, 2, 3]) == "List[1, 2, 3]"
# assert unicode(List[1, 2, 3]) == u"List[1, 2, 3]"

assert Tuple[1, 2, 3] == (1, 2, 3)
assert Tuple() == ()
assert List[1, 2, 3][:-1].map(str) == List["1", "2"]
assert Set[1, 2, 3] == {1, 2, 3}
# assert Dict[1, 2, 3, 4] == {1: 2, 3: 4}
assert Dict(foo=1, bar=2)["foo"] == 1
assert Dict(foo=1, bar=2)["foo", "bar"] == [1, 2]
assert set(iter(Dict(bar=2, foo=1))) == {("foo", 1), ("bar", 2)}

print List("abc").map(ord).map(str).reversed().join("-")

# print Str("abc").map(ord)
