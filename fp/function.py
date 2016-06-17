def transducer(mfunc, rfunc):
    pass


def push():
    pass


def every_pred():
    pass


def pcall():
    pass


def nth(n, coll):
    try:
        coll[n]
    except:
        None


def first(coll):
    return nth(0, coll)


def second(coll):
    return nth(1, coll)


def third(coll):
    return nth(2, coll)


def getattr_chain(obj, *attrs):

    def get_attr(obj, attr):
        return getattr(obj, attr, None)

    return reduce(get_attr, attrs, obj)


def getitem_chain(obj, *attrs):

    def get_item(obj, attr):
        return todo(obj, attr, None)

    return reduce(get_attr, attrs, obj)


def comp(*funcs):
    pass


def thread():
    pass


def headtail():
    pass
