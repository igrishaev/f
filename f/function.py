
from functools import partial, wraps

import six

__all__ = (
    'pcall',
    'pcall_wraps',
    'achain',
    'ichain',
    'arr1',
    'arr2',
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
    """
    Calls a passed function handling any exceptions.

    Returns either (None, result) or (exc, None) tuple.
    """
    try:
        return None, func(*args, **kwargs)
    except Exception as e:
        return e, None


def pcall_wraps(func):
    """
    A decorator that wraps a function with `pcall` logic.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return pcall(func, *args, **kwargs)

    return wrapper


def achain(obj, *attrs):
    """
    Gets through a chain of attributes
    handling AttributeError with None value.
    """
    def get_attr(obj, attr):
        return getattr(obj, attr, None)

    return reduce(get_attr, attrs, obj)


def ichain(obj, *items):
    """
    Gets through a chain of items
    handling exceptions with None value.

    Useful for data restored from a JSON string:
    >>> ichain(data, 'result', 'users', 0, 'address', 'street')
    """

    def get_item(obj, item):
        if obj is None:
            return None
        try:
            return obj[item]
        except:
            return None

    return reduce(get_item, items, obj)


def arr1(value, *forms):
    """
    Clojure's first threading macro implementation.

    Passes a value through the forms. Each form is either
    `func` or `(func, arg2, arg2, ...)`.

    The macro puts a value in the first form as the first argument.
    The result is put into the second form as the first argument,
    and so on.

    See https://clojuredocs.org/clojure.core/->

    :param value: Initial value to process.
    :type value: any

    :param forms: A tuple of forms.
    :type forms: tuple of func|(func, arg2, arg3, ...)

    :return: A value passed through the all forms.
    :rtype: any

    """
    def reducer(value, form):

        if isinstance(form, (tuple, list)):
            func, args = form[0], form[1:]
        else:
            func, args = form, ()

        all_args = (value, ) + tuple(args)
        return func(*all_args)

    return reduce(reducer, forms, value)


def arr2(value, *forms):
    """
    Clojure's second threading macro implementation.

    The logic is the same as `thread_first`, but puts the value
    at the end of each form.

    See https://clojuredocs.org/clojure.core/->>

    :param value: Initial value to process.
    :type value: any

    :param forms: A tuple of forms.
    :type forms: tuple of func|(func, arg1, arg2, ...)

    :return: A value passed through the all forms.
    :rtype: any

    """

    def reducer(value, form):

        if isinstance(form, (tuple, list)):
            func, args = form[0], form[1:]
        else:
            func, args = form, ()

        all_args = tuple(args) + (value, )
        return func(*all_args)

    return reduce(reducer, forms, value)


def comp(*funcs):
    """
    Makes a composition of passed functions:
    >>> comp(f, g, h)(x) <==> h(g(f(x)))
    """
    def composed(value):
        return arr1(value, *funcs)

    names = (func.__name__ for func in funcs)
    composed.__name__ = "composed(%s)" % ", ".join(names)

    return composed


def every_pred(*preds):
    """
    Makes a super-predicate from the passed ones.
    A super-predicate is true only if all the child predicates
    are true. The evaluation is lazy (like bool expressions).
    """
    def composed(val):
        for pred in preds:
            if not pred(val):
                return False
        return True

    names = (pred.__name__ for pred in preds)
    composed.__name__ = "predicate(%s)" % ", ".join(names)

    return composed


def transduce(mfunc, rfunc, coll, init):
    """
    A naive try to implement Clojure's transducers.

    See http://clojure.org/reference/transducers

    :param mfunc: A map function to apply to each element.
    :type mfunc: function

    :param rfunc: A reduce function to reduce the result after map.
    :type rfunc: function

    :param coll: A collection to process.
    :type coll: list|tuple|set|dict

    :param init: An initial element for reducing function.
    :type init: any

    :return: coll ==> map ==> reduce
    :rtype: any

    """
    def reducer(result, item):
        return rfunc(result, mfunc(item))

    return reduce(reducer, coll, init)


def nth(n, coll):
    """
    Returns an Nth element of a passed collection.
    Supports iterators without `__getitem__` method.
    Returns None if no item can be gotten.
    """

    # Try to get by index first.
    if hasattr(coll, '__getitem__'):
        try:
            return coll[n]
        except IndexError:
            return None

    # Otherwise, try to iterate manually.
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


# Aliases
first = partial(nth, 0)
second = partial(nth, 1)
third = partial(nth, 2)
