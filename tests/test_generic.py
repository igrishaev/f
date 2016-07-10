
from functools import partial

import pytest

import fp


# todo test replace test redirect


def test_ok():

    gen = fp.Generic()

    @gen.extend(fp.p_int, fp.p_str)
    def foo(x, y):
        return str(x) + y

    @gen.extend(fp.p_int, fp.p_int)
    def foo(x, y):
        return x + y

    @gen.extend(fp.p_str, fp.p_str)
    def foo(x, y):
        return x + y + x + y

    @gen.extend(fp.p_str)
    def foo(x):
        return "-".join(reversed(x))

    @gen.extend()
    def foo():
        return 42

    @gen.extend(fp.p_none)
    def foo(x):
        return gen(1, 2)

    assert 3 == gen(None)

    assert "12" ==  gen(1, "2")
    assert 3 ==  gen(1, 2)
    assert "fizbazfizbaz" ==  gen("fiz", "baz")
    assert "o-l-l-e-h" == gen("hello")
    assert 42 == gen()

    with pytest.raises(TypeError):
        gen(1, 2, 3, 4)
