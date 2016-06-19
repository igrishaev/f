
from functools import partial

import pytest

import fp


# todo move to predicate module
def is_type(_type, x):
    return isinstance(x, _type)

is_int = partial(is_type, int)
is_str = partial(is_type, str)
is_none = lambda x: x is None
gt = lambda a, b: a > b
gte = lambda a, b: a >= b
lt = lambda a, b: a < b
lte = lambda a, b: a <= b
eq = lambda a, b: a == b
is_ = lambda a, b: a is b
in_ = lambda a, b: a in b


# todo test replace test redirect


def test_ok():

    gen = fp.Generic()

    @gen.extend(is_int, is_str)
    def foo(x, y):
        return str(x) + y

    @gen.extend(is_int, is_int)
    def foo(x, y):
        return x + y

    @gen.extend(is_str, is_str)
    def foo(x, y):
        return x + y + x + y

    @gen.extend(is_str)
    def foo(x):
        return "-".join(reversed(x))

    @gen.extend()
    def foo():
        return 42

    @gen.extend(is_none)
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
