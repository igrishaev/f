
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
    assert l1.reduce(lambda a, b: a + b, 1) == 7

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

    # todo slice


def test_constructor():
    l = f.L((1, 2, 3))
    assert [1, 2, 3] == l

    l = f.L[1, 2, 3]
    assert [1, 2, 3] == l

    l = f.L[1]
    assert [1] == l


# def test_unicode():

#     u = f.U(u"test")
#     assert u == u"test"

#     # res = u.join('-')
#     # assert res == u"t-e-s-t"
#     # assert isinstance(res, f.Unicode)

#     res = u.map(unicode.upper)
#     print res
