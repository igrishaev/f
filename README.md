
# `f` library is a set of functional tools for Python

## Functions

A bunch of useful functions to work with data structures.

### Protected call (comes from Lua):

```python

import f

f.pcall(lambda a, b: a / b, 4, 2)
>>> (None, 2)

f.pcall(lambda a, b: a / b, 4, 0)
>>> (ZeroDivisionError('integer division or modulo by zero'), None)

func = f.pcall_wraps(lambda a, b: a / b)

func(4, 2)
>>> (None, 2)

func(4, 0)
>>> (ZeroDivisionError('integer division or modulo by zero'), None)

```

### Attribute and item chain functions handling exceptions:

```python
# let's say, you have a schema with the following foreign keys:
# Order --> Office --> Department --> Chief

order = Order.objects.get(id=42)

# OK
f.achain(model, 'office', 'department', 'chief', 'name')
>>> John

# Now imagine the `department` field is nullable and has NULL in the DB:
f.achain(model, 'office', 'department', 'chief', 'name')
>>> None
```

```python
data = json.loads('{"result": [{"kids": [{"age": 7, "name": "Leo"}, {"age": 1, "name": "Ann"}], "name": "Ivan"}, {"kids": null, "name": "Juan"}]}')

# OK
f.ichain(data, 'result', 0, 'kids', 0, 'age')
>>> 7

# the chain is broken
f.ichain(data, 'result', 42, 'kids', 0, 'age')
>> None
```

### Threading functions from Clojure

The first threading macro puts the value into an each form as a first
argument to a function:

```python
f.arr1(
    -42,                        # initial value
    (lambda a, b: a + b, 2),    # form
    abs,                        # form
    str,                        # form
    (str.replace, "40", "__")   # form
)
>>> "__"
```

The second threading macro is just the same, but puts a value at the end:

```python
f.arr2(
    -2,
    abs,
    (lambda a, b: a + b, 2),
    str,
    ("000".replace, "0")
)
>>> "444"
```

### Function composition:

```python
comp = f.comp(abs, (lambda x: x * 2), str)
comp(-42)
>>> "84"
```

### Every predicate

Composes a super predicate from the passed ones:

```python
pred1 = f.p_gt(0)
pred2 = f.p_even
pred3 = f.p_not_eq(666)

every = f.every_pred(pred1, pred2, pred3)

result = filter(every, (-1, 1, -2, 2, 3, 4, 666, -3, 1, 2))
tuple(result)
>>> (2, 4, 2)
```

### Transducer: a quick-and-dirty port from Clojure

```python
f.transduce(
    (lambda x: x + 1),
    (lambda res, item: res + str(item)),
    (1, 2, 3),
    ""
)
>>> "234"
```

### Nth element getters

```python
f.first((1, 2, 3))
>>> 1

f.second((1, 2, 3))
>>> 2

f.third((1, 2, 3))
>>> 3

f.nth(0, [1, 2, 3])
>>> 1

f.nth(9, [1, 2, 3])
>>> None
```

## Predicates

A set of unary and binary predicates.

Unary example:

```python
f.p_str("test")
>>> True

f.p_str(0)
>>> False

f.p_str(u"test")
>>> True

# checks for both int and float types
f.p_num(1), f.p_num(1.0)
>>> True, True

f.p_list([])
>>> True

f.p_truth(1)
>>> True

f.p_truth(None)
>>> False

f.p_none(None)
>>> True
```

Binary example:

```python
p = f.p_gt(0)

p(1), p(100), p(0), p(-1)
>>> True, True, False, False

p = f.p_gte(0)
p(0), p(1), p(-1)
>>> True, True, False

p = f.p_eq(42)
p(42), p(False)
>>> True, False

ob1 = object()
p = f.p_is(ob1)
p(object())
>>> False
p(ob1)
>>> True

p = f.p_in((1, 2, 3))
p(1), p(3)
>>> True, True
p(4)
>>> False
```

You may combine predicates with `f.comp` or `f.every_pred`:

```python
# checks for positive even number
pred = f.every_pred(f.p_num, f.p_even, f.p_gt(0))
pred(None), pred(-1), pred(5)
>>> False, False, False
pred(6)
>>> True
```

## Collections

Improved collections `List`, `Typle`, `Dict` and `Set` with the following
features.

### Square braces syntax for initiating

```python
f.List[1, 2, 3]     # or just f.L
>>> List[1, 2, 3]

f.T[1, 2, 3]
>>> Tuple(1, 2, 3)

f.Set[1, 2, 3]
>>> Set{1, 2, 3}

f.D[1: 2, 2: 3]
>>> Dict{1: 2, 2: 3}
```

### Additional methods such as .map, .filter, .foreach, .sum, etc:

```python

l1 = f.L[1, 2, 3]
assert l1.map(str).join("-") == "1-2-3"
```

### Cevery method returns a new collection of this type:

  todo

### Easy adding two collection of different types

  todo

### Quick turning to another collection

  todo


## Monads

Maybe, Either, Error and IO monads are implemented.

### Maybe

```python
MaybeInt = f.maybe(f.p_int)
MaybeInt(2)
>>> Just[2]
```

### Either

### IO


## Generics

Generic is a flexible callable object that may have different strategies
depending on a set of predicates (guards).

```python
# create an instance
gen = f.Generic()

# extend it with handlers
@gen.extend(f.p_int, f.p_str)
def handler1(x, y):
    return str(x) + y

@gen.extend(f.p_int, f.p_int)
def handler2(x, y):
    return x + y

@gen.extend(f.p_str, f.p_str)
def handler3(x, y):
    return x + y + x + y

@gen.extend(f.p_str)
def handler4(x):
    return "-".join(reversed(x))

@gen.extend()
def handler5():
    return 42

@gen.extend(f.p_none)
def handler6(x):
    return gen(1, 2)

# let's try:
gen(None)
>>> 3

gen(1, "2")
>>> "12"

gen(1, 2)
>>> 3

gen("fiz", "baz")
>>> "fizbazfizbaz"

gen("hello")
>>> "o-l-l-e-h"

gen()
>>> 42

# calling without a default handler
gen(1, 2, 3, 4)
>>> TypeError exception goes here...

# now we have one
@gen.default
def default_handler(*args):
    return "default"

gen(1, 2, 3, 4)
>>> "default"
```
