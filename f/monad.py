
import sys
from functools import wraps

__all__ = (

    'Maybe',
    'Either',
    'Try',
    'IO',
    'maybe_decorator',
    'either_decorator',
    'try_decorator',
    'io_decorator',
)


class Maybe(object):

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

    class Meta(type):

        def __getitem__(cls, tp):

            @wraps(Maybe)
            def wrapper(val):

                if isinstance(val, tp):
                    return Maybe.Just(val)

                else:
                    return Maybe.Nothing()

            return wrapper

    __metaclass__ = Meta

    def __init__(self):
        raise NotImplementedError


class Either(object):

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

    class Meta(type):

        def __getitem__(cls, (tp_l, tp_r)):

            @wraps(Either)
            def wrapper(val):

                if isinstance(val, tp_l):
                    return Either.Left(val)

                if isinstance(val, tp_r):
                    return Either.Right(val)

                msg = ('Value %s is neither <%s> nor <%s> instance.'
                       % (val, tp_l.__name__, tp_r.__name__))
                raise TypeError(msg)

            return wrapper

    __metaclass__ = Meta

    def __init__(self):
        raise NotImplementedError


class Try(object):

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

    def __new__(cls, func, *args, **kwargs):

        try:
            return Try.Success(func(*args, **kwargs))

        except Exception as e:
            return Try.Failture(e)

        except:
            e_cls, e_val, e_tb = sys.exc_info()
            return Try.Failture(e_val)


class IO(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def __rshift__(self, func):
        return func(self.__val)

    def get(self):
        return self.__val


def maybe_decorator(cls):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            val = func(*args, **kwargs)
            return Maybe[cls](val)

        return wrapper

    return decorator


def either_decorator(type_left, type_right):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            val = func(*args, **kwargs)
            return Either[type_left, type_right](val)

        return wrapper

    return decorator


def try_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return Try(func, *args, **kwargs)

    return wrapper


def io_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return IO(func(*args, **kwargs))

    return wrapper
