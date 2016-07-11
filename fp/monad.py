
__all__ = (
    # 'Monad',

    'Maybe',
    'Just',
    'Nothing',

    'Either',
    'Left',
    'Right',

    'Try',
    'Success',
    'Failture',
)


# class Monad(object):

#     def __init__(self, *args, **kwargs):
#         raise NotImplementedError

#     @classmethod
#     def unit(cls, val):
#         return cls(val)

#     def bind(self, func):
#         raise NotImplementedError

#     def __rshift__(self, func):
#         return self.__class__.bind(self, func)


class Maybe(object):

    def __new__(cls, val=None):
        if val is None:
            return Nothing()
        else:
            return Just(val)

    @classmethod
    def from_value(cls, val):
        return cls(val)

    @classmethod
    def from_call(cls, func, *args, **kwargs):
        val = func(*args, **kwargs)
        return cls.from_value(val)


class Just(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def bind(self, func):
        return func(self.__val)

    def get(self):
        return self.__val

    def __iter__(self):
        yield self.__val

    __rshift__ = bind


class Nothing(object):

    def __init__(self):
        pass

    def bind(self, func):
        return self

    def get(self):
        return None

    def __iter__(self):
        raise StopIteration

    __rshift__ = bind


class Either(object):

    def __new__(cls, val):
        return Right(val)


# class LeftRightBase(object):

#     __slots__ = ('__val', )

#     def __init__(self, val):
#         self.__val = val


class Left(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def bind(self, func):
        return self

    __rshift__ = bind


class Right(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def bind(self, func):
        return func(self.__val)

    __rshift__ = bind


class Try(object):

    def __new__(cls, func, *args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return Success(val)
        except Exception as e:
            return Failture(e)
        # except:
        #     # todo


class Success(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def bind(self, func):
        return func(self.__val)

    __rshift__ = bind

    def get(self):
        return self.__val

    def recover(self, exc_class, val_or_func):
        return self


class Failture(object):

    __slots__ = ('__val', )

    def __init__(self, val):
        self.__val = val

    def bind(self, func):
        return self

    __rshift__ = bind

    def get(self):
        raise self.__val

    def recover(self, exc_class, val_or_func):

        def is_callable(val):
            return hasattr(val_or_func, '__call__')

        def resolve():

            if is_callable(val_or_func):
                return val_or_func(e)

            else:
                return val_or_func

        e = self.__val

        if isinstance(e, exc_class):
            return Success(resolve())

        else:
            return self
