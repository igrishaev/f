
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


# def obj_data():
#     class

def double(a):
    return a * 2


def plus(a, b):
    """
    Adds two numbers.
    """
    return a + b


def div(a, b):
    return a / b


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
    # todo
    pass


def test_ichain_ok():
    data = json_data()
    assert 7 == fp.ichain(data, 'result', 0, 'kids', 0, 'age')


def test_ichain_missing():
    data = json_data()
    assert fp.ichain(data, 'foo', 'bar', 999, None) is None


def test_thread_ok():
    # todo
    assert "42" == fp.thread(-42, abs, str)


def test_thread_complex():
    # todo
    pass


def test_comp():
    comp = fp.comp(abs, double, str)
    assert "84" == comp(-42)


def test_comp_name():
    comp = fp.comp(abs, double, str)
    assert "composed(abs, double, str)" in comp.__name__


def test_every_pred():
    pass
