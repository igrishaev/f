
import math

import f

import pytest
import six

#
# helpers
#


@f.maybe_wraps(f.p_num)
def mdiv(a, b):
    if b:
        return a / b
    else:
        return None


@f.maybe_wraps(f.p_num)
def msqrt(a):
    if a >= 0:
        return math.sqrt(a)
    else:
        return None


@f.either_wraps(f.p_str, f.p_num)
def ediv(a, b):
    if b == 0:
        return "Div by zero: %s / %s" % (a, b)
    else:
        return a / b


@f.either_wraps(f.p_str, f.p_num)
def esqrt(a):
    if a < 0:
        return "Negative number: %s" % a
    else:
        return math.sqrt(a)


@f.error_wraps
def tdiv(a, b):
    return a / b


@f.error_wraps
def tsqrt(a):
    return math.sqrt(a)


@pytest.mark.parametrize("x,val", (
    (2, f.Just),
    (2.0, f.Just),
    (-2, f.Nothing),
))
def test_maybe_laws(x, val):

    p = f.p_num
    unit = f.maybe(p)

    @f.maybe_wraps(p)
    def g(x):
        if x > 0:
            return x * 2
        else:
            return None

    @f.maybe_wraps(p)
    def h(x):
        if x > 0:
            return x + 2
        else:
            return None

    assert isinstance(g(x), val)

    # 1
    assert unit(x) >> g == g(x)

    # 2
    mv = g(x)
    assert mv >> unit == mv

    # 3
    (mv >> g) >> h == mv >> (lambda x: g(x) >> h)


def test_maybe():

    unit = f.maybe(f.p_int)

    m = unit(42)
    assert isinstance(m, f.Just)

    assert 42 == m.get()

    m = unit(None)
    assert isinstance(m, f.Nothing)

    m = mdiv(16, 4) >> msqrt
    assert isinstance(m, f.Just)

    m = mdiv(16, 4.0) >> msqrt
    assert isinstance(m, f.Just)
    assert 2 == m.get()

    m = mdiv(16, 0) >> msqrt
    assert isinstance(m, f.Nothing)
    assert None is m.get()

    m = mdiv(16, -4) >> msqrt
    assert isinstance(m, f.Nothing)


def test_either():

    unit = f.either(f.p_str, f.p_num)

    m = unit("error")
    assert isinstance(m, f.Left)
    # assert "error" == m.get()

    m = unit(42)
    assert isinstance(m, f.Right)
    # assert 42 == m.get()

    m = ediv(16, 4) >> esqrt
    assert isinstance(m, f.Right)
    # assert 2 == m.get()

    m = ediv(16, -4) >> esqrt
    assert isinstance(m, f.Left)
    # assert "Negative number: -4" == m.get()

    m = ediv(16, 0) >> esqrt
    assert isinstance(m, f.Left)
    # assert "Div by zero: 16 / 0" == m.get()


@pytest.mark.parametrize("x,val", (
    (2, f.Right),
    (2.0, f.Right),
    (-2, f.Left),
))
def test_either_laws(x, val):

    p = (f.p_str, f.p_num)
    unit = f.either(*p)

    @f.either_wraps(*p)
    def g(x):
        if x > 0:
            return x + 2
        else:
            return "less the zero"

    @f.either_wraps(*p)
    def h(x):
        if x > 0:
            return x + 3
        else:
            return "less the zero2"

    assert isinstance(g(x), val)

    # 1
    assert unit(x) >> g == g(x)

    # 2
    mv = g(x)
    assert mv >> unit == mv

    # 3
    (mv >> g) >> h == mv >> (lambda x: g(x) >> h)


def test_error():

    unit = f.error(lambda a, b: a / b)

    m = unit(16, b=4)
    assert isinstance(m, f.Success)

    assert 4 == m.get()

    m = unit(16, b=0)
    assert isinstance(m, f.Failture)

    with pytest.raises(ZeroDivisionError):
        m.get()


def test_failture():

    unit = f.error(lambda: 1 / 0)

    m = unit()
    res = m.recover(ZeroDivisionError, 0)
    assert isinstance(res, f.Success)

    assert 0 == res.get()

    with pytest.raises(ZeroDivisionError):
        m.get()

    res = m.recover(MemoryError, 0)
    assert isinstance(res, f.Failture)


def test_failture_recover_multi():

    unit = f.error(lambda: 1 / 0)

    m = unit()
    res = m \
        .recover(MemoryError, 1) \
        .recover(TypeError, 2) \
        .recover(ValueError, 3)

    assert isinstance(res, f.Failture)

    def handler(exc):
        return exc.__class__.__name__

    res2 = res.recover((AttributeError, ZeroDivisionError), handler)
    assert isinstance(res2, f.Success)
    assert "ZeroDivisionError" == res2.get()


def test_success_recover():

    unit = f.error(lambda: 1)
    m = unit().recover(Exception, 0)
    assert isinstance(m, f.Success)
    assert 1 == m.get()


def test_try_decorator():

    m = tdiv(16, 4) >> tsqrt
    assert isinstance(m, f.Success)
    assert 2 == m.get()

    m = tdiv(16, 0) >> tsqrt
    assert isinstance(m, f.Failture)
    with pytest.raises(ZeroDivisionError):
        m.get()

    m = tdiv(16, -4) >> tsqrt
    assert isinstance(m, f.Failture)
    with pytest.raises(ValueError):
        m.get()


def test_io(monkeypatch, capsys):

    if six.PY2:
        path = '__builtin__.raw_input'

    if six.PY3:
        path = 'builtins.input'

    monkeypatch.setattr(path, lambda prompt: "hello")

    @f.io_wraps
    def read_line(prompt):
        if six.PY2:
            return raw_input("say: ")
        if six.PY3:
            return input("say: ")

    @f.io_wraps
    def write_line(text):
        six.print_(text)

    res = read_line("test: ") >> write_line
    assert isinstance(res, f.IO)
    assert None is res.get()

    out, err = capsys.readouterr()
    assert "hello\n" == out
    assert "" == err


def test_maybe_unit():

    Maybe = f.maybe(f.p_int)

    m = Maybe(42)
    assert isinstance(m, f.Just)
    assert 42 == m.get()

    m = Maybe("error")
    assert isinstance(m, f.Nothing)
    assert None is m.get()


def test_either_unit():

    Either = f.either(f.p_str, f.p_num)

    m = Either(42)
    assert isinstance(m, f.Right)
    assert 42 == m.get()

    m = Either("error")
    assert isinstance(m, f.Left)
    assert "error" == m.get()

    with pytest.raises(TypeError):
        Either(None)
