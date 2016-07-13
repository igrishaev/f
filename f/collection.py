
import six

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
    """
    Todo
    """

    def join(self, sep=""):
        return sep.join(self)

    # lt todo
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

    def reduce(self, init, fn, *args, **kwargs):

        def reducer(res, item):
            return fn(res, item, *args, **kwargs)

        return six.moves.reduce(reducer, self, init)

    # lt todo
    def sorted(self, key=None):
        return self.cls(sorted(self, key=key))

    # lt todo
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

    # lt todo
    def apply(self, fn):
        return fn(*self)

    def sum(self):
        return sum(self)

    # lt
    def group(self, n=2):
        range = six.moves.range
        gen = (self[i: i+n] for i in range(0, len(self), n))
        return self.cls(gen)

    def __add__(self, other):

        def gen():

            for x in self:
                yield x

            for y in self.cls(other):
                yield y

        return self.cls(gen())

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


class LTmixin(object):
    """
    List and Tuple features.
    """

    def __getitem__(self, item):
        """
        Performs accessing value by index.

        If a slice was passed, turn the result
        into the current collection type.
        """
        result = super(LTmixin, self).__getitem__(item)

        if isinstance(item, slice):
            return self.__class__(result)
        else:
            return result

    # PY2 only method
    def __getslice__(self, *args):
        result = super(LTmixin, self).__getslice__(*args)
        return self.__class__(result)


class LTSMeta(type):

    def __getitem__(cls, args):
        """
        Triggers when accessing a collection class by index, e.g:
        >>> List[1, 2, 3]
        """
        if isinstance(args, tuple):
            return cls(args)
        else:
            return cls((args, ))


@six.add_metaclass(LTSMeta)
class LTSmixin(object):
    """
    List, Tuple and Set features.
    """
    pass


class List(Seq, LTSmixin, LTmixin, list):
    pass


class Tuple(Seq, LTSmixin, LTmixin, tuple):
    pass


class Set(Seq, LTSmixin, set):
    pass


class DictMeta(type):

    def __getitem__(cls, slices):
        """
        A nice hack: when you pass a dict body in square braces,
        you'll receive a tuple if slices.
        """

        if isinstance(slices, tuple):
            slice_tuple = slices
        else:
            slice_tuple = (slices, )

        keys = (sl.start for sl in slice_tuple)
        vals = (sl.stop for sl in slice_tuple)

        return cls(zip(keys, vals))


@six.add_metaclass(DictMeta)
class Dict(Seq, dict):

    def __iter__(self):
        """
        I'd like to iterate a dict by (key, val) pairs.
        """
        if six.PY2:
            return iter(self.iteritems())

        if six.PY3:
            return iter(self.items())


# Short aliases
L = List
T = Tuple
S = Set
D = Dict
