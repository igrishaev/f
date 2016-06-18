
from functools import wraps

__all__ = (
    'pcall',
    'pcall_decorator',
    'achain',
    'ichain',
    'thread',
    'comp',
    'every_pred',
)


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


def thread(value, *funcs):

    def reducer(value, func):
        return func(value)

    return reduce(reducer, funcs, value)


# def thread2(value):
#     pass


def comp(*funcs):

    def composed(value):
        return thread(value, *funcs)

    names = (func.__name__ for func in funcs)
    composed.__name__ = "composed(%s)" % ", ".join(names)

    return composed


def every_pred(*preds):

    # todo name
    def composed(val):
        for pred in preds:
            if not pred(val):
                return False
        return True

    return composed


def nth(n, coll):
    try:
        coll[n]
    except:
        None


def first(coll):
    return nth(0, coll)


def second(coll):
    return nth(1, coll)


def third(coll):
    return nth(2, coll)


def headtail():
    pass


# def transducer(mfunc, rfunc):
#     pass


# def push():
#     pass
