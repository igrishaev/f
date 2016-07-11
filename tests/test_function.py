
import pytest

import fp


#
# helpers
#


def json_data():
    return {
        "result": [
            {"name": "Ivan", "kids": [
                {"name": "Leo", "age": 7},
                {"name": "Ann", "age": 1},
            ]},
            {"name": "Juan", "kids": None},
        ]
    }


def double(a):
    return a * 2


def inc(a):
    return a + 1


def plus(a, b):
    """
    Adds two numbers.
    """
    return a + b


def div(a, b):
    return a / b


class Foo:
    class Bar:
        class Baz:
            secret = 42


#
# tests
#


def test_pcall_ok():
    assert (None, 3) == fp.pcall(plus, 1, 2)


def test_pcall_err():
    err, result = fp.pcall(div, 1, 0)
    assert result is None
    assert isinstance(err, ZeroDivisionError)


def test_pcall_arity_err():
    err, result = fp.pcall(plus, 1, 2, 1)
    assert result is None
    assert isinstance(err, TypeError)


def test_pcall_decorator():

    safe_div = fp.pcall_decorator(div)
    assert (None, 2) == safe_div(10, 5)

    err, result = safe_div(10, 0)
    assert result is None
    assert isinstance(err, ZeroDivisionError)


def test_pcall_decorator_name():
    safe_div = fp.pcall_decorator(div)
    assert safe_div.__name__ == div.__name__


def test_achain():
    assert 42 == fp.achain(Foo, 'Bar', 'Baz', 'secret')


def test_achain_missed():
    assert fp.achain(Foo, 'Bar', 'Bob', 'secret') is None


def test_ichain_ok():
    data = json_data()
    assert 7 == fp.ichain(data, 'result', 0, 'kids', 0, 'age')


def test_ichain_missing():
    data = json_data()
    assert fp.ichain(data, 'foo', 'bar', 999, None) is None


def test_thread_first():
    assert "990" == fp.thread_first(
        -42,
        (plus, 2),
        (div, 4),
        abs,
        str,
        (str.replace, "1", "99")
    )


def test_thread_last():
    result = fp.thread_last(
        -2,
        abs,
        (div, 100),
        (plus, 2),
        str,
        ("000".replace, "0")
    )
    assert "525252" == result


def test_comp():
    comp = fp.comp(abs, double, str)
    assert "84" == comp(-42)


def test_comp_name():
    comp = fp.comp(abs, double, str)
    assert "composed(abs, double, str)" in comp.__name__


def test_every_pred():

    pred1 = fp.p_gt(0)
    pred2 = fp.p_even
    pred3 = fp.p_not_eq(666)

    every = fp.every_pred(pred1, pred2, pred3)

    result = filter(every, (-1, 1, -2, 2, 3, 4, 666, -3, 1, 2))
    assert (2, 4, 2) == result


def test_every_pred_lazy():

    def pred1(x):
        return False

    def pred2(x):
        raise ValueError("some error")

    every = fp.every_pred(pred1, pred2)

    result = filter(every, (-1, 1, -2, 2, 3, 4, 666, -3, 1, 2))
    try:
        assert () == result
    except ValueError:
        pytest.fail("Should not be risen!")


def test_every_pred_name():

    def is_positive(x):
        return x > 0

    def is_even(x):
        return x % 2 == 0

    every = fp.every_pred(is_positive, is_even)
    assert "predicate(is_positive, is_even)" in str(every)


def test_transduce():

    result = fp.transduce(
        inc,
        (lambda res, item: res + str(item)),
        (1, 2, 3),
        ""
    )
    assert "234" == result


def test_transduce_comp():

    result = fp.transduce(
        fp.comp(abs, inc, double),
        (lambda res, item: res + (item, )),
        [-1, -2, -3],
        ()
    )

    assert (4, 6, 8) == result


def test_first():
    assert 1 == fp.first((1, 2, 3))


def test_second():
    assert 2 == fp.second((1, 2, 3))


def test_third():
    assert 3 == fp.third((1, 2, 3))


def test_nth():
    assert 1 == fp.nth(0, [1, 2, 3])
    assert None is fp.nth(9, [1, 2, 3])


def test_nth_no_index():
    assert 1 == fp.nth(0, set([1]))
    assert None is fp.nth(2, set([1]))
