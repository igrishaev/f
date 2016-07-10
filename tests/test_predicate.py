
import fp


def test_unary():

    assert fp.p_str("test")
    assert fp.p_str(0) is False
    assert fp.p_str(u"test") is False

    assert fp.p_ustr(u"test")

    assert fp.p_num(1)
    assert fp.p_num(1.0)
    assert fp.p_num(1L)

    assert fp.p_array([1, 2, 3])
    assert fp.p_array((1, 2, 3))

    assert fp.p_truth(1)
    assert fp.p_truth(None) is False
    assert fp.p_truth([]) is False

    assert fp.p_none(None)
    assert fp.p_none(42) is False


def test_binary():

    p = fp.p_gt(0)
    assert p(1)
    assert p(100)
    assert p(0) is False
    assert p(-1) is False

    p = fp.p_gte(0)
    assert p(0)
    assert p(1)
    assert p(-1) is False

    p = fp.p_eq(42)
    assert p(42)
    assert p(False) is False

    p = fp.p_not_eq(42)
    assert p(42) is False
    assert p(False)

    ob1 = object()
    p = fp.p_is(ob1)
    assert p(object()) is False
    assert p(ob1)

    p = fp.p_in((1, 2, 3))
    assert p(1)
    assert p(3)
    assert p(4) is False

    p = fp.p_and(False)
    assert p(True) is False
    assert p(False) is False

    p = fp.p_or(42)
    assert p(0) == 42
    assert p(1) == 1
