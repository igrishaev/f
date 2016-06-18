
__all__ = (
    # todo
)


def cons():
    pass


class Cons(object):

    def __init__(self, l, r=None):
        self.l = l
        self.r = r

    class Meta(type):

        def __getitem__(self, args):
            pass
            # return reduce(, args)
            # for arg
            # return Set(args)

    __metaclass__ = Meta



class ConsList(object):
    pass


def car():
    pass


def cdr():
    pass
