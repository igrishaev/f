
import math

import f

import pytest

#
# helpers
#


@f.maybe_decorator((int, float))
def mdiv(a, b):
    if b:
        return a / b
    else:
        return None


@f.maybe_decorator(float)
def msqrt(a):
    if a >= 0:
        return math.sqrt(a)
    else:
        return None


@f.either_decorator(str, (int, float))
def ediv(a, b):

    if b == 0:
        return "Div by zero: %s / %s" % (a, b)

    else:
        return a / b


@f.either_decorator(str, float)
def esqrt(a):

    if a < 0:
        return "Negative number: %s" % a

    else:
        return math.sqrt(a)


def test_maybe():

    with pytest.raises(NotImplementedError):
        f.Maybe()

    Maybe = f.Maybe[int]

    m = Maybe(42)
    assert isinstance(m, Maybe.Just)

    m = Maybe(None)
    assert isinstance(m, Maybe.Nothing)

    m = mdiv(16, 4) >> msqrt
    assert isinstance(m, Maybe.Just)

    m = mdiv(16, 4.0) >> msqrt
    assert isinstance(m, Maybe.Just)
    assert 2 == m.get()

    m = mdiv(16, 0) >> msqrt
    assert isinstance(m, Maybe.Nothing)
    assert None is m.get()

    m = mdiv(16, -4) >> msqrt
    assert isinstance(m, Maybe.Nothing)


def test_either():

    with pytest.raises(NotImplementedError):
        f.Either()

    Either = f.Either[str, int]

    m = Either("error")
    assert isinstance(m, Either.Left)
    assert "error" == m.get()

    m = Either(42)
    assert isinstance(m, Either.Right)
    assert 42 == m.get()

    m = ediv(16, 4) >> esqrt
    assert isinstance(m, Either.Right)
    assert 2 == m.get()

    m = ediv(16, -4) >> esqrt
    assert isinstance(m, Either.Left)
    assert "Negative number: -4" == m.get()

    m = ediv(16, 0) >> esqrt
    assert isinstance(m, Either.Left)
    assert "Div by zero: 16 / 0" == m.get()


def test_try():

    Try = f.Try

    m = Try((lambda a, b: a / b), 16, b=4)
    assert isinstance(m, Try.Success)

    assert 4 == m.get()

    m = Try((lambda a, b: a / b), 16, b=0)
    assert isinstance(m, Try.Failture)

    with pytest.raises(ZeroDivisionError):
        m.get()


def test_failture():

    m = f.Try(lambda: 1 / 0)

    res = m.recover(ZeroDivisionError, 0)
    assert isinstance(res, f.Try.Success)

    assert 0 == res.get()

    with pytest.raises(ZeroDivisionError):
        m.get()

    res = m.recover(MemoryError, 0)
    assert isinstance(res, f.Try.Failture)


def test_generic_exc():

    import socket

    def raiser():
        raise socket.error('old-style-exc')

    m = f.Try(raiser)
    assert isinstance(m, f.Try.Failture)

    res = m.recover(socket.error, 42)
    assert isinstance(res, f.Try.Success)


def test_failture_recover_multi():

    m = f.Try(lambda: 1 / 0)

    res = m \
        .recover(MemoryError, 1) \
        .recover(TypeError, 2) \
        .recover(ValueError, 3)

    assert isinstance(res, f.Try.Failture)

    def handler(exc):
        return exc.__class__.__name__

    res2 = res.recover((AttributeError, ZeroDivisionError), handler)
    assert isinstance(res2, f.Try.Success)
    assert "ZeroDivisionError" == res2.get()


def test_success_recover():

    m = f.Try(lambda: 1).recover(Exception, 0)
    assert isinstance(m, f.Try.Success)
    assert 1 == m.get()


def test_try_decorator():

    @f.try_decorator
    def div(a, b):
        return a / b

    @f.try_decorator
    def sqrt(a):
        return math.sqrt(a)

    m = div(16, 4) >> sqrt
    assert isinstance(m, f.Try.Success)
    assert 2 == m.get()

    m = div(16, 0) >> sqrt
    assert isinstance(m, f.Try.Failture)
    with pytest.raises(ZeroDivisionError):
        m.get()

    m = div(16, -4) >> sqrt
    assert isinstance(m, f.Try.Failture)
    with pytest.raises(ValueError):
        m.get()


def test_io(monkeypatch, capsys):

    monkeypatch.setattr('__builtin__.raw_input',
                        (lambda prompt: "hello"))

    @f.io_decorator
    def read_line(prompt):
        return raw_input(prompt)

    @f.io_decorator
    def write_line(text):
        print text

    res = read_line("test: ") >> write_line
    assert isinstance(res, f.IO)
    assert None is res.get()

    out, err = capsys.readouterr()
    assert "hello\n" == out
    assert "" == err


def test_maybe_unit():

    Maybe = f.Maybe[int]

    m = Maybe(42)
    assert isinstance(m, Maybe.Just)
    assert 42 == m.get()

    m = Maybe("error")
    assert isinstance(m, Maybe.Nothing)
    assert None is m.get()


def test_():

    Either = f.Either[str, int]

    m = Either(42)
    assert isinstance(m, Either.Right)
    assert 42 == m.get()

    m = Either("error")
    assert isinstance(m, Either.Left)
    assert "error" == m.get()

    with pytest.raises(TypeError):
        Either(None)
