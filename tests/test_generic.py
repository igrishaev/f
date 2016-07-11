
import pytest

import fp


@pytest.yield_fixture
def gen():

    gen = fp.Generic()

    @gen.extend(fp.p_int, fp.p_str)
    def handler1(x, y):
        return str(x) + y

    @gen.extend(fp.p_int, fp.p_int)
    def handler2(x, y):
        return x + y

    @gen.extend(fp.p_str, fp.p_str)
    def handler3(x, y):
        return x + y + x + y

    @gen.extend(fp.p_str)
    def handler4(x):
        return "-".join(reversed(x))

    @gen.extend()
    def handler5():
        return 42

    @gen.extend(fp.p_none)
    def handler6(x):
        return gen(1, 2)

    yield gen


def test_ok(gen):

    assert 3 == gen(None)
    assert "12" == gen(1, "2")
    assert 3 == gen(1, 2)
    assert "fizbazfizbaz" == gen("fiz", "baz")
    assert "o-l-l-e-h" == gen("hello")
    assert 42 == gen()


def test_no_handler(gen):

    with pytest.raises(TypeError):
        gen(1, 2, 3, 4)


def test_default(gen):

    @gen.default
    def default_handler(*args):
        return "default"

    assert "default" == gen(1, 2, 3, 4)


def test_handler_is_gen(gen):

    @gen.extend(fp.p_dict)
    def handler8(x):
        return 100500

    assert handler8 is gen
    assert 100500 == handler8({})
