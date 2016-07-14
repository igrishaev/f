
import pytest

import f


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


class Rabbit:
    class Duck:
        class Egg:
            class Needle:
                class Death:
                    on = True


#
# tests
#


def test_pcall_ok():
    assert (None, 3) == f.pcall(plus, 1, 2)


def test_pcall_err():
    err, result = f.pcall(div, 1, 0)
    assert result is None
    assert isinstance(err, ZeroDivisionError)


def test_pcall_arity_err():
    err, result = f.pcall(plus, 1, 2, 1)
    assert result is None
    assert isinstance(err, TypeError)


def test_pcall_wraps():

    safe_div = f.pcall_wraps(div)
    assert (None, 2) == safe_div(10, 5)

    err, result = safe_div(10, 0)
    assert result is None
    assert isinstance(err, ZeroDivisionError)


def test_pcall_wraps_name():
    safe_div = f.pcall_wraps(div)
    assert safe_div.__name__ == div.__name__


def test_achain():
    assert True is f.achain(
        Rabbit, 'Duck', 'Egg', 'Needle', 'Death', 'on')


def test_achain_missed():
    assert None is f.achain(
        Rabbit, 'Duck', 'Egg', 'Needle', 'Life', 'on')


def test_ichain_ok():
    data = json_data()
    assert 7 == f.ichain(data, 'result', 0, 'kids', 0, 'age')


def test_ichain_missing():
    data = json_data()
    assert f.ichain(data, 'foo', 'bar', 999, None) is None


def test_arr1():
    assert "__" == f.arr1(
        -42,
        (plus, 2),
        abs,
        str,
        (str.replace, "40", "__")
    )


def test_arr2():
    result = f.arr2(
        -2,
        abs,
        (plus, 2),
        str,
        ("000".replace, "0")
    )
    assert "444" == result


def test_comp():
    comp = f.comp(abs, double, str)
    assert "84" == comp(-42)


def test_comp_name():
    comp = f.comp(abs, double, str)
    assert "composed(abs, double, str)" in comp.__name__


def test_every_pred():

    pred1 = f.p_gt(0)
    pred2 = f.p_even
    pred3 = f.p_not_eq(666)

    every = f.every_pred(pred1, pred2, pred3)

    result = filter(every, (-1, 1, -2, 2, 3, 4, 666, -3, 1, 2))
    assert (2, 4, 2) == tuple(result)


def test_every_pred_lazy():

    def pred1(x):
        return False

    def pred2(x):
        raise ValueError("some error")

    every = f.every_pred(pred1, pred2)

    result = filter(every, (-1, 1, -2, 2, 3, 4, 666, -3, 1, 2))
    try:
        assert () == tuple(result)
    except ValueError:
        pytest.fail("Should not be risen!")


def test_every_pred_name():

    def is_positive(x):
        return x > 0

    def is_even(x):
        return x % 2 == 0

    every = f.every_pred(is_positive, is_even)
    assert "predicate(is_positive, is_even)" in str(every.__name__)


def test_transduce():

    result = f.transduce(
        inc,
        (lambda res, item: res + str(item)),
        (1, 2, 3),
        ""
    )
    assert "234" == result


def test_transduce_comp():

    result = f.transduce(
        f.comp(abs, inc, double),
        (lambda res, item: res + (item, )),
        [-1, -2, -3],
        ()
    )

    assert (4, 6, 8) == result


def test_first():
    assert 1 == f.first((1, 2, 3))


def test_second():
    assert 2 == f.second((1, 2, 3))


def test_third():
    assert 3 == f.third((1, 2, 3))


def test_nth():
    assert 1 == f.nth(0, [1, 2, 3])
    assert None is f.nth(9, [1, 2, 3])


def test_nth_no_index():
    assert 1 == f.nth(0, set([1]))
    assert None is f.nth(2, set([1]))
