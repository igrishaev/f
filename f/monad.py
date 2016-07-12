
import sys
from functools import wraps

__all__ = (
    'Just',
    'Nothing',
    'Left',
    'Right',
    'Success',
    'Failture',
    'IO',
    'maybe',
    'maybe_wraps',
    'either',
    'either_wraps',
    'error',
    'error_wraps',
    'io_wraps',
)


class Just(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return func(self.__val)

    def get(self):
        return self.__val


class Nothing(object):

    def __rshift__(self, func):
        return self

    def get(self):
        return None


class Left(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return self

    def get(self):
        return self.__val


class Right(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return func(self.__val)

    def get(self):
        return self.__val


class Success(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return func(self.__val)

    def get(self):
        return self.__val


class Failture(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return self

    def get(self):
        raise self.__val


class IO(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return func(self.__val)

    def get(self):
        return self.__val


def maybe(pred):

    def maybe_unit(x):

        if pred(x):
            return Just(x)

        else:
            return Nothing()

    return maybe_unit


def maybe_wraps(pred):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return maybe(pred)(func(*args, **kwargs))

        return wrapper

    return decorator


def either(pred_l, pred_r):

    def either_unit(x):

        if pred_l(x):
            return Left(x)

        if pred_r(x):
            return Right(x)

        raise TypeError("todo")

    return either_unit


def either_wraps(pred_l, pred_r):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return either(pred_l, pred_r)(func(*args, **kwargs))

        return wrapper

    return decorator


def error(func, *args, **kwargs):
    try:
        return Success(func(*args, **kwargs))
    except Exception as e:
        return Failture(e)
    except:
        _, e_val, _ = sys.exc_info()
        return Failture(e_val)


def error_wraps(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return error(func, *args, **kwargs)

    return wrapper


def io_wraps(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return IO(func(*args, **kwargs))

    return wrapper
