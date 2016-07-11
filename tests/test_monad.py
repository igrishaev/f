
import math

import fp

import pytest

#
# helpers
#


def mdiv(a, b):
    if b:
        return fp.Just(a / b)
    else:
        return fp.Nothing()


def msqrt(a):
    if a >= 0:
        return fp.Just(math.sqrt(a))
    else:
        return fp.Nothing()


def ediv(a, b):
    if b:
        return fp.Right(a / b)
    else:
        return fp.Left("Div by zero: %s / %s" % (a, b))


def esqrt(a):
    if a >= 0:
        return fp.Right(math.sqrt(a))
    else:
        return fp.Left("Negative number: %s" % a)


def test_maybe():

    m = fp.Maybe.from_value(1)
    assert isinstance(m, fp.Just)

    m = fp.Maybe.from_value(None)
    assert isinstance(m, fp.Nothing)

    m = fp.Maybe.from_call((lambda a, b=0: a / b), 16, b=4)
    assert isinstance(m, fp.Just)

    m = fp.Maybe.from_call(lambda: None)
    assert isinstance(m, fp.Nothing)

    m = fp.Maybe(42)
    assert isinstance(m, fp.Just)

    m = fp.Just(1)
    assert isinstance(m, fp.Just)

    m = fp.Maybe(None)
    assert isinstance(m, fp.Nothing)

    m = fp.Nothing()
    assert isinstance(m, fp.Nothing)

    m = mdiv(16, 4) >> msqrt
    assert isinstance(m, fp.Just)

    m = mdiv(16, 0) >> msqrt
    assert isinstance(m, fp.Nothing)

    m = mdiv(16, -4) >> msqrt
    assert isinstance(m, fp.Nothing)


def test_either():

    # todo test from call and value

    assert isinstance(fp.Either(42), fp.Right)
    assert isinstance(fp.Either(None), fp.Right)

    m = fp.Right(123)
    assert isinstance(m, fp.Right)

    m = fp.Left(123)
    assert isinstance(m, fp.Left)

    m = ediv(16, 4) >> esqrt
    assert isinstance(m, fp.Right)

    m = ediv(16, -4) >> esqrt
    assert isinstance(m, fp.Left)

    m = ediv(16, 0) >> esqrt
    assert isinstance(m, fp.Left)


def test_try():

    m = fp.Try((lambda a, b: a / b), 16, b=4)
    assert isinstance(m, fp.Success)

    assert 4 == m.get()

    m = fp.Try((lambda a, b: a / b), 16, b=0)
    assert isinstance(m, fp.Failture)

    with pytest.raises(ZeroDivisionError):
        m.get()

    def getKey1(x):
        return fp.Just(123)

    def getKey2(x):
        return fp.Just(321)

    def getData(x, y):
        return fp.Just(x + y)

    # getKey1("123") \
    #     >> (lambda key1: getKey2(key1)) \
    #     >> (lambda key2: getData(key1, key2)) \
    #     >> (lambda data: printData(data))

    res = getKey1("123") >> \
          (lambda key1: getKey2(key1) >> \
           (lambda key2: getData(key1, key2)))
    print res

    # for key1 in getKey1("123"):
    #     for key2 in key1 >> getKey2:
    #         for data in getData

    # for (
    #         key1 for key1 in getKey1("123"),
    #         key2 for key2 in key1 >> getKey2,
    #         data for getData()
    # )
