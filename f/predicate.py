

import operator
from functools import partial, wraps

import six

__all__ = (
    "p_gt",
    "p_gte",
    "p_lt",
    "p_lte",
    "p_eq",
    "p_not_eq",
    "p_in",
    "p_is",
    "p_is_not",
    "p_and",
    "p_or",
    "p_inst",

    "p_str",
    "p_int",
    "p_float",
    "p_num",
    "p_list",
    "p_tuple",
    "p_set",
    "p_dict",
    "p_array",
    "p_coll",
    "p_truth",
    "p_none",
    "p_not_none",
    "p_even",
    "p_odd",
)

#
# Binary
#


def _binary(func, b):
    """
    A basic form of binary predicate.

    `func` is a two-argument function.
    `b` is a second argument.

    Returns a function that takes the first argument
    and returns a bool value.
    """
    @wraps(func)
    def wrapper(a):
        return func(a, b)

    return wrapper


p_gt = partial(_binary, operator.gt)
p_gte = partial(_binary, operator.ge)
p_lt = partial(_binary, operator.lt)
p_lte = partial(_binary, operator.le)
p_eq = partial(_binary, operator.eq)
p_not_eq = partial(_binary, (lambda a, b: a != b))
p_in = partial(_binary, (lambda x, coll: x in coll))
p_is = partial(_binary, operator.is_)
p_is_not = partial(_binary, operator.is_not)
p_and = partial(_binary, (lambda a, b: a and b))
p_or = partial(_binary, (lambda a, b: a or b))
p_inst = partial(_binary, isinstance)

#
# Unary
#

p_str = p_inst(six.string_types)
p_int = p_inst(six.integer_types)
p_float = p_inst(float)
p_num = p_inst(six.integer_types + (float, ))
p_list = p_inst(list)
p_tuple = p_inst(tuple)
p_set = p_inst(set)
p_dict = p_inst(dict)
p_array = p_inst((list, tuple))
p_coll = p_inst((list, tuple, dict, set))


def p_truth(x):
    return bool(x) is True


def p_none(x):
    return x is None


def p_not_none(x):
    return x is not None


def p_even(x):
    return x % 2 == 0


def p_odd(x):
    return x % 2 != 0
