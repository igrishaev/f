
import f


def test_unary():

    assert f.p_str("test")
    assert f.p_str(0) is False
    assert f.p_str(u"test") is False

    assert f.p_ustr(u"test")

    assert f.p_num(1)
    assert f.p_num(1.0)
    assert f.p_num(1L)

    assert f.p_array([1, 2, 3])
    assert f.p_array((1, 2, 3))

    assert f.p_truth(1)
    assert f.p_truth(None) is False
    assert f.p_truth([]) is False

    assert f.p_none(None)
    assert f.p_none(42) is False


def test_binary():

    p = f.p_gt(0)
    assert p(1)
    assert p(100)
    assert p(0) is False
    assert p(-1) is False

    p = f.p_gte(0)
    assert p(0)
    assert p(1)
    assert p(-1) is False

    p = f.p_eq(42)
    assert p(42)
    assert p(False) is False

    p = f.p_not_eq(42)
    assert p(42) is False
    assert p(False)

    ob1 = object()
    p = f.p_is(ob1)
    assert p(object()) is False
    assert p(ob1)

    p = f.p_in((1, 2, 3))
    assert p(1)
    assert p(3)
    assert p(4) is False

    p = f.p_and(False)
    assert p(True) is False
    assert p(False) is False

    p = f.p_or(42)
    assert p(0) == 42
    assert p(1) == 1
