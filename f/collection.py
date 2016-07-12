
__all__ = (
    'List',
    'Tuple',
    'Set',
    'Dict',
    'L',
    'T',
    'S',
    'D',
)


class Seq(object):

    def join(self, sep=""):
        return sep.join(self)

    def reversed(self):
        return self.cls(reversed(self))

    def foreach(self, func, *args, **kwargs):
        for item in self:
            func(item, *args, **kwargs)

    def map(self, fn, *args, **kwargs):

        def process(item):
            return fn(item, *args, **kwargs)

        return self.cls(map(process, self))

    def filter(self, pred, *args, **kwargs):

        def criteria(item):
            return pred(item, *args, **kwargs)

        return self.cls(filter(criteria, self))

    def reduce(self, fn, init, *args, **kwargs):

        def reducer(res, item):
            return fn(res, item, *args, **kwargs)

        return reduce(reducer, self, init)

    def sorted(self, key=None):
        return self.cls(sorted(self, key=key))

    def distinct(self):

        cache_hash = set()
        cache_list = []

        def is_hashable(x):
            return getattr(x, '__hash__', None) is not None

        def cache_set(x):
            if is_hashable(x):
                cache_hash.add(x)
            else:
                cache_list.append(x)

        def cache_has(x):
            if is_hashable(x):
                return x in cache_hash
            else:
                return x in cache_list

        res = []

        def process(x):
            if not cache_has(x):
                cache_set(x)
                res.append(x)

        self.foreach(process)

        return self.cls(res)

    def apply(self, fn):
        return fn(*self)

    def sum(self):
        return sum(self)

    def group(self, n=2):
        gen = (self[i: i+n] for i in xrange(0, len(self), n))
        return self.cls(gen)

    def __add__(self, other):
        cls = self.cls
        adder = self.super.__add__
        return cls(adder(cls(other)))

    def __repr__(self):
        to_repr = self.super.__repr__
        return "%s%s" % (self.cls.__name__, to_repr())

    @property
    def super(self):
        return super(Seq, self)

    @property
    def cls(self):
        return self.__class__

    def Tuple(self):
        return Tuple(self)

    def List(self):
        return List(self)

    def Set(self):
        return Set(self)

    def Dict(self):
        return Dict(self)

    L = List
    T = Tuple
    S = Set
    D = Dict


class Foo(object):
    pass


class List(Seq, Foo, list):

    class Meta(type):

        def __getitem__(self, args):
            if isinstance(args, tuple):
                return List(args)
            else:
                return List((args, ))

    __metaclass__ = Meta

    def __getslice__(self, *args, **kwargs):
        getslice = super(List, self).__getslice__
        return List(getslice(*args, **kwargs))


class Tuple(Seq, tuple):

    class Meta(type):

        def __getitem__(self, args):
            return Tuple(args)

    __metaclass__ = Meta


class Dict(dict, Seq):

    class Meta(type):

        def __getitem__(self, foo):
            pass
            # import ipdb; ipdb.set_trace()
            # print foo
            # return Dict((arg.start, arg.stop) for arg in foo)

    __metaclass__ = Meta

    __iter__ = dict.iteritems

    def __getitem__(self, items):
        getter = super(Dict, self).__getitem__
        if isinstance(items, tuple):
            return map(getter, items)
        else:
            return getter(items)


class Set(set):

    class Meta(type):

        def __getitem__(self, args):
            return Set(args)

    __metaclass__ = Meta


# class Str(Seq, str):
#     pass


# class Unicode(Seq, unicode):
#     pass


L = List
T = Tuple
S = Set
D = Dict
