
from functools import partial, wraps

import six

__all__ = (
    'pcall',
    'pcall_decorator',
    'achain',
    'ichain',
    'thread_first',
    'thread_last',
    'comp',
    'every_pred',
    'transduce',
    'nth',
    'first',
    'second',
    'third',
)

reduce = six.moves.reduce
range = six.moves.range


def pcall(func, *args, **kwargs):
    try:
        return None, func(*args, **kwargs)
    except Exception as e:
        return e, None


def pcall_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return pcall(func, *args, **kwargs)

    return wrapper


def achain(obj, *attrs):

    def get_attr(obj, attr):
        return getattr(obj, attr, None)

    return reduce(get_attr, attrs, obj)


def ichain(obj, *items):

    def get_item(obj, item):
        if obj is None:
            return None
        try:
            return obj[item]
        except:
            return None

    return reduce(get_item, items, obj)


def thread_first(value, *forms):

    def reducer(value, form):

        if isinstance(form, (tuple, list)):
            func, args = form[0], form[1:]
        else:
            func, args = form, ()

        all_args = (value, ) + tuple(args)
        return func(*all_args)

    return reduce(reducer, forms, value)


def thread_last(value, *forms):

    def reducer(value, form):

        if isinstance(form, (tuple, list)):
            func, args = form[0], form[1:]
        else:
            func, args = form, ()

        all_args = tuple(args) + (value, )
        return func(*all_args)

    return reduce(reducer, forms, value)


def comp(*funcs):

    def composed(value):
        return thread_first(value, *funcs)

    names = (func.__name__ for func in funcs)
    composed.__name__ = "composed(%s)" % ", ".join(names)

    return composed


def every_pred(*preds):

    def composed(val):
        for pred in preds:
            if not pred(val):
                return False
        return True

    names = (pred.__name__ for pred in preds)
    composed.__name__ = "predicate(%s)" % ", ".join(names)

    return composed


def transduce(mfunc, rfunc, coll, init):

    def reducer(result, item):
        return rfunc(result, mfunc(item))

    return reduce(reducer, coll, init)


def nth(n, coll):

    # try to get by index first
    if hasattr(coll, '__getitem__'):
        try:
            return coll[n]
        except IndexError:
            return None

    # otherwise, try to iterate manualy
    elif hasattr(coll, '__iter__'):

        iterator = iter(coll)
        for x in range(n + 1):
            try:
                val = next(iterator)
            except StopIteration:
                return None
        return val

    else:
        return None


first = partial(nth, 0)
second = partial(nth, 1)
third = partial(nth, 2)
