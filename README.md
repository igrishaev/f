
### `f` library is a set of functional tools for Python

#### Functions

A bunch of useful functions to work with data structures.

- Protected call (comes from Lua):

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

- Attribute and item chain functions handling exceptions:

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

- Threading functions came from Clojure

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

- Function composition:

```python
comp = f.comp(abs, (lambda x: x * 2), str)
comp(-42)
>>> "84"
```

- Every predicate

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

- Transducer:



### Predicates

### Collections

Improved collections `List`, `Typle`, `Dict` and `Set` with the
following features:

- Square braces syntax for initiating:

```
f.L[1, 2, 3]  # or f.List
>>> List[1, 2, 3]

f.T[1, 2, 3]
>>> Tuple(1, 2, 3)

f.Set[1, 2, 3]
>>> Set{1, 2, 3}

f.D[1: 2, 2: 3]
>>> Dict{1: 2, 2: 3}
```

- additional methods such as .map, .filter, reduce, .sorted, .foreach,
  .sum, etc:

    l1 = f.L[1, 2, 3]
    assert l1.map(str).join("-") == "1-2-3"

    todo

- every method returns a new collection of this type:

  todo

- easy adding two collection of different types:

  todo

- quick turning to another collection:

  todo


### Monads

Maybe, Either, Error and IO monads are implemented.

#### Maybe

MaybeInt = f.maybe(f.p_int)
MaybeInt(2)
>>> Just[2]

todo


#### Either


#### IO



### Generics

Generic as a flexible callable object that may have different
strategies depending on a set of predicates (guards).

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
