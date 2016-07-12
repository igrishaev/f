
import f


def test_list():

    l1 = f.L[1, 2, 3]
    assert l1 == [1, 2, 3]

    l2 = l1.map(str)
    assert l2 == ["1", "2", "3"]
    assert isinstance(l2, f.L)
    assert l1 == [1, 2, 3]

    assert l1.map(str).join("-") == "1-2-3"

    result = []

    def collect(x, delta=0):
        result.append(x + delta)

    l1.foreach(collect, delta=1)
    assert result == [2, 3, 4]

    def inc(x, delta=1):
        return x + delta

    l2 = l1.map(inc, delta=2)
    assert l2 == [3, 4, 5]
    assert isinstance(l2, f.L)

    l2 = l1.filter(f.p_even)
    assert l2 == [2]
    assert isinstance(l2, f.L)

    # todo
    assert l1.reduce(1, (lambda a, b: a + b)) == 7

    assert l1.sum() == 6

    def summer(*nums):
        return sum(nums)

    assert l1.apply(summer) == 6

    res = l1 + (1, 2, 3)
    assert res == [1, 2, 3, 1, 2, 3]
    assert isinstance(res, f.L)

    assert str(l1) == "List[1, 2, 3]"
    assert unicode(l1) == u"List[1, 2, 3]"

    t1 = l1.T()
    assert t1 == (1, 2, 3)
    assert isinstance(t1, f.Tuple)

    l2 = l1.group(2)
    assert l2 == [[1, 2], [3]]
    assert isinstance(l2, f.L)

    el1, el2 = l2
    assert isinstance(el1, f.L)
    assert isinstance(el2, f.L)

    d1 = f.L["a", 1, "b", 2].group(2).D()
    assert d1 == {"a": 1, "b": 2}
    assert isinstance(d1, f.D)

    res = f.L[3, 3, 2, 1, 1, 3, 2, 2, 3].distinct()
    assert [3, 2, 1] == res
    assert isinstance(res, f.L)

    res = f.L[{1: 2}, {1: 2}, {1: 3}].distinct()
    assert [{1: 2}, {1: 3}] == res
    assert isinstance(res, f.L)

    res = f.L[3, 2, 1, 1, 2, 3].sorted()
    assert [1, 1, 2, 2, 3, 3] == res
    assert isinstance(res, f.L)

    res = f.L[(3, 1), (2, 2), (1, 3)].sorted(key=(lambda (a, b): a))
    assert [(1, 3), (2, 2), (3, 1)] == res
    assert isinstance(res, f.L)


def test_list_constructor():

    l = f.L((1, 2, 3))
    assert [1, 2, 3] == l

    l = f.L[1, 2, 3]
    assert [1, 2, 3] == l

    l = f.L[1]
    assert [1] == l


def test_tuple_constructor():

    t = f.T([1, 2, 3])
    assert (1, 2, 3) == t
    assert isinstance(t, f.T)

    t = f.T[1, 2, 3]
    assert (1, 2, 3) == t
    assert isinstance(t, f.T)

    t = f.T[1]
    assert (1, ) == t
    assert isinstance(t, f.T)


def test_set_constructor():

    s = f.S((1, 2, 3))
    assert {1, 2, 3} == s
    assert isinstance(s, f.S)

    s = f.S[1, 2, 3]
    assert {1, 2, 3} == s
    assert isinstance(s, f.S)

    s = f.S[1]
    assert {1} == s
    assert isinstance(s, f.S)


def test_list_slice():

    res = f.L[1, 2, 3][:1]
    assert [1] == res
    assert isinstance(res, f.L)


def test_tuple_slice():

    res = f.T[1, 2, 3][:1]
    assert (1, ) == res
    assert isinstance(res, f.T)


def test_set_features():

    s = f.S[1, 2, 3]

    assert {"1", "2", "3"} == s.map(str)

    assert f.S["a", "b"].join("-") in ("a-b", "b-a")

    res = s.filter(f.p_even)
    assert {2} == res
    assert isinstance(res, f.S)

    assert 106 == s.reduce(100, (lambda res, x: res + x))

    assert 6 == s.sum()

    res = s + ["a", 1, "b", 3, "c"]
    assert {1, 2, 3, "a", "b", "c"} == res
    assert isinstance(res, f.S)

    assert {1, 2, 3} == s

    # assert {(1, 2), 3} == s.group(2)


def test_dict_features():

    d = f.D(a=1, b=2, c=3)
    res = d + dict(d=4, e=5, f=5)

    assert dict(a=1, b=2, c=3) == d
    assert res == dict(a=1, b=2, c=3, d=4, e=5, f=5)
    assert isinstance(res, f.D)


def test_dict_constructor():

    # d = f.D["name": "Ivan", "sex": "male"]
    pass


# def test_unicode():

#     u = f.U(u"test")
#     assert u == u"test"

#     # res = u.join('-')
#     # assert res == u"t-e-s-t"
#     # assert isinstance(res, f.Unicode)

#     res = u.map(unicode.upper)
#     print res


# tests

# assert List[1, 2, 3] + (4, 5, 6) == List[1, 2, 3, 4, 5, 6]
# assert List[1, 2, 3].Tuple() == Tuple[1, 2, 3]
# assert List[1, 2, 3].map(str).Tuple() == Tuple["1", "2", "3"]
# assert List[1, 2, 3].apply(lambda *args: sum(args)) == 6
# assert List[1, 2, 3].reduce(0, (lambda res, x: res + x)) == 6
# assert List[1, 2, 3].reduce((), (lambda res, x: res + (x, ))) == (1, 2, 3)

# assert str(List[1, 2, 3]) == "List[1, 2, 3]"
# # assert unicode(List[1, 2, 3]) == u"List[1, 2, 3]"

# assert Tuple[1, 2, 3] == (1, 2, 3)
# assert Tuple() == ()
# assert List[1, 2, 3][:-1].map(str) == List["1", "2"]
# assert Set[1, 2, 3] == {1, 2, 3}
# # assert Dict[1, 2, 3, 4] == {1: 2, 3: 4}
# assert Dict(foo=1, bar=2)["foo"] == 1
# assert Dict(foo=1, bar=2)["foo", "bar"] == [1, 2]
# assert set(iter(Dict(bar=2, foo=1))) == {("foo", 1), ("bar", 2)}

# print List("abc").map(ord).map(str).reversed().join("-")

# print Str("abc").map(ord)
