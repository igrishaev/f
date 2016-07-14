
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

range = six.moves.range
filter = six.moves.filter


class SeqMixin(object):
    """
    A basic mixin for all types of collections.

    It provides additional methods and changes
    collection's behaviour.
    """

    def join(self, sep=""):
        """
        Joins a collection into a string.

        Note: turn items to strings before using map:
        >>> coll.map(str).join(',')
        """
        return sep.join(self)

    def foreach(self, func, *args, **kwargs):
        """
        Performs a function with additional arguments
        for each element without returning a result.
        """
        for item in self:
            func(item, *args, **kwargs)

    def map(self, fn, *args, **kwargs):
        """
        Returns a new collection of this type
        without changing an existing one.

        Each element is a result of applying a passed function
        to corresponding element of an old collection.
        """
        def process(item):
            return fn(item, *args, **kwargs)

        return self.__class__(map(process, self))

    def filter(self, pred, *args, **kwargs):

        def criteria(item):
            return pred(item, *args, **kwargs)

        return self.__class__(filter(criteria, self))

    def reduce(self, init, fn, *args, **kwargs):
        """
        Returns a new filtered collection.
        """
        def reducer(res, item):
            return fn(res, item, *args, **kwargs)

        return six.moves.reduce(reducer, self, init)

    def sum(self):
        """
        Adds all the elements together.

        Turn items to numbers first using map:
        >>> coll.map(int).sum()
        """
        return sum(self)

    def __add__(self, other):
        """
        Adds a two collection together. Returns a new collection
        without changing old ones.

        The other collection might be a different type.
        It will be converted to the current type.
        """
        def gen():
            for x in self:
                yield x
            for y in self.__class__(other):
                yield y

        return self.__class__(gen())

    def __repr__(self):
        """
        Just like a parent __repr__, but with a leading prefix:
        >>> List[1, 2, 3], Dict{1: 2, 3: 4}, etc
        """
        old_repr = super(SeqMixin, self).__repr__()
        return "%s%s" % (self.__class__.__name__, old_repr)

    # Shortcuts to turn a collection into another type.
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

    def reversed(self):
        """
        Returns a new collection in a reserved order.
        """
        return self.__class__(reversed(self))

    def sorted(self, key=None):
        """
        Returns a new sorted collection.

        Without passing a key functions, it returns as-is.
        A key function is a two-argument function that determes
        sorting logic.
        """
        return self.__class__(sorted(self, key=key))

    def group(self, n=2):
        """
        Returns a new collections with items grouped by N:
        >>> L[1, 2, 3].group(2) ==> L[L[1, 2], L[3]]
        """
        gen = (self[i: i+n] for i in range(0, len(self), n))
        return self.__class__(gen)

    def distinct(self):
        """
        Returns a new collection without duplicates.

        We don't use set(...) trick here to keep previous order.
        It supports non-hashable elements such as dicts or lists.
        """

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

        return self.__class__(res)

    def apply(self, fn):
        """
        Passes all the items as *args to a function
        and gets the result.
        """
        return fn(*self)


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


class List(SeqMixin, LTSmixin, LTmixin, list):
    pass


class Tuple(SeqMixin, LTSmixin, LTmixin, tuple):
    pass


class Set(SeqMixin, LTSmixin, set):

    def __repr__(self):
        old_repr = set.__repr__(self)
        return "Set{%s}" % old_repr[5:-2]


class DictMeta(type):

    def __getitem__(cls, slices):
        """
        Builds a dict having a tuple of slices.
        """

        if isinstance(slices, tuple):
            slice_tuple = slices
        else:
            slice_tuple = (slices, )

        keys = (sl.start for sl in slice_tuple)
        vals = (sl.stop for sl in slice_tuple)

        return cls(zip(keys, vals))


@six.add_metaclass(DictMeta)
class Dict(SeqMixin, dict):

    def __iter__(self):
        """
        Iterates a dict by (key, val) pairs.
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
