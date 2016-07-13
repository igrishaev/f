
__all__ = (
    'Generic',
)


class Generic(object):
    """
    Generic implementation.

    Usage:

    gen = f.Generic()

    @gen.extend(f.p_int, f.p_str)
    def handler1(x, y):
        return str(x) + y

    @gen.extend(f.p_int, f.p_int)
    def handler2(x, y):
        return x + y

    @gen.default
    def default_handler(*args):
        return "default"

    gen(1, "2")
    >>> "12"

    gen(1, 2, 3, 4)
    >>> "default"

    """

    __slots__ = ("__funcs", "__default", )

    def __init__(self):
        self.__funcs = {}
        self.__default = None

    def extend(self, *preds):
        """
        Extends the generic with a handler function.

        :param preds: A tuple of predicates for each argument.
        :type preds: tuple of func(x) -> bool

        :return: This generic
        :rtype: f.Generic

        """

        def wrapper(func):
            self.__funcs[preds] = func
            return self

        return wrapper

    def default(self, func):
        """
        Registers the default handler for generic.

        The function should deal with any kind of arguments.

        :param func: A function default logic.
        :type func: function

        :return: This generic
        :rtype: f.Generic

        """

        self.__default = func
        return self

    def __call__(self, *args):

        for preds in self.__funcs:
            if len(preds) == len(args):
                pairs = zip(preds, args)
                if all(func(arg) for (func, arg) in pairs):
                    return self.__funcs[preds](*args)

        if self.__default:
            return self.__default(*args)
        else:
            msg = "No function was found for such arguments: %s" % args
            raise TypeError(msg)
