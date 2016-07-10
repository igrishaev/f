
__all__ = (
    'Generic',
)


class Generic(object):

    def __init__(self):
        self.__funcs = {}
        self.__default = None

    def extend(self, *preds):

        def wrapper(func):
            self.__funcs[preds] = func
            return self

        return wrapper

    def default(self, func):
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
            raise TypeError("No function was found for such arguments")
