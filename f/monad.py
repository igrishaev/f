
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

    def recover(self, exc_class, val_or_func):
        return self


class Failture(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return self

    def get(self):
        raise self.__val

    def recover(self, exc_class, val_or_func):

        e = self.__val

        def is_callable(val):
            return hasattr(val_or_func, '__call__')

        def resolve():

            if is_callable(val_or_func):
                return val_or_func(e)

            else:
                return val_or_func

        if isinstance(e, exc_class):
            return Try.Success(resolve())

        else:
            return self


class IO(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return func(self.__val)

    def get(self):
        return self.__val


def maybe(cls):

    def _maybe(x):

        if isinstance(x, cls):
            return Right(x)

        else:
            return Nothing()

    return _maybe


def maybe_wraps(cls):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            val = func(*args, **kwargs)
            return maybe(cls)(val)

        return wrapper

    return decorator


def either(cls_l, cls_r):

    def _either(x):

        if isinstance(x, cls_l):
            return Left(x)

        if isinstance(x, cls_r):
            return Right(x)

        raise TypeError("todo")

    return _either


def either_wraps(cls_l, cls_r):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            val = func(*args, **kwargs)
            return either(cls_l, cls_r)(val)

        return wrapper

    return decorator


def error(func, *args, **kwargs):
    try:
        return Success(func(*args, **kwargs))
    except Exception as e:
        return Failture(e)


def error_wraps(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return error(func, *args, **kwargs)

    return wrapper


# def io(func, *args, **kwargs):
#     return IO()
#     try:
#         return Success(func(*args, **kwargs))
#     except Exception as e:
#         return Failture(e)


def io_wraps(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        return IO(cls_l, cls_r)(val)

    return wrapper
