
import operator
from functools import partial, wraps

# todo __all__

#
# Binary
#


def _binary(func, b):

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


#
# Unary
#


def _unary(func):

    @wraps(func)
    def predicate(x):
        return func(x)

    return predicate


def _inst(*cls):

    def predicate(x):
        return isinstance(x, cls)

    return predicate


p_str = _unary(_inst(str))
p_ustr = _unary(_inst(unicode))
p_any_str = _unary(_inst(str, unicode))
p_int = _unary(_inst(int))
p_float = _unary(_inst(float))
p_long = _unary(_inst(long))
p_num = _unary(_inst(int, long, float))
p_list = _unary(_inst(list))
p_tuple = _unary(_inst(tuple))
p_set = _unary(_inst(set))
p_dict = _unary(_inst(dict))
p_array = _unary(_inst(list, tuple))
p_coll = _unary(_inst(list, tuple, dict, set))
p_truth = _unary(lambda x: bool(x) is True)
p_none = _unary(lambda x: x is None)
p_not_none = _unary(lambda x: x is not None)
p_even = _unary(lambda x: x % 2 == 0)
p_odd = _unary(lambda x: x % 2 != 0)
