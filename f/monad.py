
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
    'io',
    'io_wraps',
)


class Monad(object):

    __slots__ = ('_val', )

    def __init__(self, val):
        self._val = val

    def __rshift__(self, form):

        if isinstance(form, (list, tuple)):
            func, args = form[0], form[1:]
        else:
            func = form
            args = ()

        return func(self._val, *args)

    def bind(self, *form):
        return self >> form

    def __eq__(self, other):
        """
        Compares two monadic values by their type and content.
        """
        return (
            type(self) == type(other)
            and self._val == other._val
        )

    def __repr__(self):
        return "%s[%s]" % (self.__class__.__name__, self._val)

    def get(self):
        return self._val


class Nothing(Monad):
    """
    Represents a negative Maybe value.
    """

    def __init__(self):
        pass

    def __rshift__(self, func):
        """
        Always returns current object without performing
        a passed function.
        """
        return self

    def __eq__(self, other):
        return isinstance(other, Nothing)

    def __repr__(self):
        return self.__class__.__name__

    def get(self):
        return None


class Just(Monad):
    """
    Represents a positive Maybe value.
    """
    pass


class Left(Monad):
    """
    Represents a negative Either value.
    """

    def __rshift__(self, func):
        return self


class Right(Monad):
    """
    Represents a positive Either value.
    """
    pass


class Success(Monad):
    """
    Represents a positive Error value.
    """

    def recover(self, exc_class, val_or_func):
        """
        Does nothing, returning the current monadic value.
        """
        return self


class Failture(Monad):
    """
    Represents a negative Error value.
    """

    def __rshift__(self, func):
        return self

    def get(self):
        raise self._val

    def recover(self, exc_class, val_or_func):
        """
        Recovers an exception.

        :param exc_class: An exception class or a tuple of classes to recover.
        :type exc_class: Exception|tuple of Exception

        :param val_or_func: A value or a function to get a positive result.
        :type val_or_func: any|function

        :return: Success instance if the cought exception matches `exc_class`
                 or Failture if it does not.
        :rtype: Failture|Success

        Usage:

        error(lambda: 1 / 0).recover(Exception, 42).get()
        >>> 42

        """

        e = self._val

        def is_callable(val):
            return hasattr(val_or_func, '__call__')

        def resolve():

            if is_callable(val_or_func):
                return val_or_func(e)

            else:
                return val_or_func

        if isinstance(e, exc_class):
            return Success(resolve())

        else:
            return self


class IO(Monad):
    """
    Represents IO value.
    """
    pass


def maybe(pred):
    """
    Maybe constructor.

    Takes a predicate and returns a function
    that receives `x` and returns a Maybe instance of `x`.

    :param pred: a function that determines if a value is Just or Nothing.
    :type pred: function

    :return: Maybe unit function.
    :rtype: function

    """
    def maybe_unit(x):
        """
        Maybe unit.

        :param x: Any non-monadic value.
        :type x: any

        :return: Monadic value.
        :rtype: Just|Nothing

        """
        if pred(x):
            return Just(x)

        else:
            return Nothing()

    return maybe_unit


def maybe_wraps(pred):
    """
    Decorator that wraps a function with maybe behaviour.
    """
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return maybe(pred)(func(*args, **kwargs))

        return wrapper

    return decorator


def either(pred_l, pred_r):
    """
    Either constructor.

    Takes two predicates and returns a function
    that receives `x` and returns an Either instance of `x`.

    :param pred_l: Left predicate.
    :type pred_l: function

    :param pred_r: Right predicate.
    :type pred_r: function

    :return: Either unit function.
    :rtype: function

    """

    def either_unit(x):
        """
        Either unit.

        :param x: Any non-monadic value.
        :type x: any

        :return: Monadic value.
        :rtype: Left|Right

        """

        if pred_l(x):
            return Left(x)

        if pred_r(x):
            return Right(x)

        msg = "Value %s doesn't fit %s nor %s predicates."
        params = (x, pred_l, pred_r)

        raise TypeError(msg % params)

    return either_unit


def either_wraps(pred_l, pred_r):
    """
    Decorator that wraps a function with either behaviour.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return either(pred_l, pred_r)(func(*args, **kwargs))

        return wrapper

    return decorator


def error(func):
    """
    Error constructor.

    Takes a function with additional arguments. Calls the function
    handling any possible exceptions. Returns either `Success`
    with actual value or `Failture` with an exception instance inside.

    :param func: A function to call.
    :type func: function

    :param args: A tuple of positional parameters
    :type args: tuple of any

    :param kwargs: A dict of named parameters.
    :type kwargs: dict of any

    :return: Monadic value of Error
    :rtype: Success|Failture

    """

    def error_unit(*args, **kwargs):
        try:
            return Success(func(*args, **kwargs))
        except Exception as e:
            return Failture(e)

    return error_unit


error_wraps = error


def io(func):
    """
    Decorator that wraps a function with IO behaviour.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        return IO(func(*args, **kwargs))

    return wrapper


io_wraps = io
