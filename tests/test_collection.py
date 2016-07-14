
import f

import six


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

    assert l1.reduce(1, (lambda a, b: a + b)) == 7
    assert f.L[1, 2, 3].reduce((), (lambda res, x: res + (x, ))) == (1, 2, 3)

    assert l1.sum() == 6

    def summer(*nums):
        return sum(nums)

    assert l1.apply(summer) == 6

    res = l1 + (1, 2, 3)
    assert res == [1, 2, 3, 1, 2, 3]
    assert isinstance(res, f.L)

    assert six.text_type(l1) == "List[1, 2, 3]"

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

    res = f.L[(3, 1), (2, 2), (1, 3)].sorted(key=(lambda pair: pair[0]))
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
    assert set((1, 2, 3)) == s
    assert isinstance(s, f.S)

    s = f.S[1, 2, 3]
    assert set((1, 2, 3)) == s
    assert isinstance(s, f.S)

    s = f.S[1]
    assert set((1, )) == s
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

    assert set(("1", "2", "3")) == s.map(str)

    assert f.S["a", "b"].join("-") in ("a-b", "b-a")

    res = s.filter(f.p_even)
    assert set((2, )) == res
    assert isinstance(res, f.S)

    assert 106 == s.reduce(100, (lambda res, x: res + x))

    assert 6 == s.sum()

    res = s + ["a", 1, "b", 3, "c"]
    assert set((1, 2, 3, "a", "b", "c")) == res
    assert isinstance(res, f.S)

    assert set((1, 2, 3)) == s


def test_dict_features():

    d = f.D(a=1, b=2, c=3)
    res = d + dict(d=4, e=5, f=5)

    assert dict(a=1, b=2, c=3) == d
    assert res == dict(a=1, b=2, c=3, d=4, e=5, f=5)
    assert isinstance(res, f.D)

    def my_filter(pair):
        key, val = pair
        return key == 1 and val == 1

    d = f.D[2: 3, 3: 1, 1: 1]
    d2 = d.filter(my_filter)
    assert d2 == {1: 1}
    assert isinstance(d2, f.D)


def test_dict_constructor():

    d = f.D["foo": 42]
    assert dict(foo=42) == d

    d = f.D["name": "Juan", "sex": "male", 1: 42, None: [1, 2, 3]]
    assert {"name": "Juan", "sex": "male", 1: 42, None: [1, 2, 3]} == d
    assert isinstance(d, f.D)

    d = f.D["foo": f.D["bar": f.D["baz": 42]]]
    node = d["foo"]["bar"]
    assert isinstance(node, f.D)
    assert 42 == node["baz"]

    assert "Dict{'foo': Dict{'bar': Dict{'baz': 42}}}" == six.text_type(d)


def test_dict_iter():
    assert list(f.D[1: 2]) == [(1, 2)]


def test_complex():
    origin = f.L[4, 3, 2, 1]

    def pred(pair):
        k, v = pair
        return k == "1" and v == "2"

    res = origin.map(str).Tuple().reversed() \
                .group(2).Dict().filter(pred)

    assert res == {"1": "2"}
    assert isinstance(res, f.D)

    assert origin == [4, 3, 2, 1]

    assert "99-98-97" == f.L("abc").map(ord).map(str).reversed().join("-")

    assert f.L[1, 2, 3].map(str).Tuple() == f.T["1", "2", "3"]
    assert f.L[1, 2, 3][:-1].map(str) == f.L["1", "2"]

    assert set(f.D(bar=2, foo=1)) == {("foo", 1), ("bar", 2)}
