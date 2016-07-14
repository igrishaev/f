# `f` is a set of functional tools for Python

## Functions

A bunch of useful functions to work with data structures.

### Protected call (comes from Lua):

```python
import f

f.pcall(lambda a, b: a / b, 4, 2)
>>> (None, 2)

f.pcall(lambda a, b: a / b, 4, 0)
>>> (ZeroDivisionError('integer division or modulo by zero'), None)
```

Or use it like a decorator:

```python

@f.pcall_wraps
def func(a, b):
    return a / b

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

# Now imagine the `department` field is null-able and has NULL in the DB:
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

Improved collections `List`, `Tuple`, `Dict` and `Set` with the following
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
l1.map(str).join("-")
>>> "1-2-3"

result = []

def collect(x, delta=0):
    result.append(x + delta)

l1.foreach(collect, delta=1)
result == [2, 3, 4]
>>> True
```

See the source code for more methods.

### Every method returns a new collection of this type:

```python
l1.filter(f.p_even)
>>> List[2]

l1.group(2)
>>> List[List[1, 2], List[3]]

# filtering a dict:
f.D[1: 1, 2: 2, 0: 2].filter(lambda (k, v): k + v == 2)
>>> Dict{0: 2, 1: 1}
```

### Easy adding two collection of different types

```python

# merging dicts
f.D(a=1, b=2, c=3) + {"d": 4, "e": 5, "f": 5}
>>> Dict{'a': 1, 'c': 3, 'b': 2, 'e': 5, 'd': 4, 'f': 5}

f.S[1, 2, 3] + ["a", 1, "b", 3, "c"]
>>> Set{'a', 1, 2, 3, 'c', 'b'}

# adding list with tuple
f.L[1, 2, 3] + (4, )
List[1, 2, 3, 4]
```

### Quick turning to another collection

```python
f.L["a", 1, "b", 2].group(2).D()
>>> Dict{"a": 1, "b": 2}

f.L[1, 2, 3, 3, 2, 1].S().T()
>>> Tuple[1, 2, 3]
```

## Monads

There are Maybe, Either, Error and IO monads are in the library. Most of them
are based on classical Haskell definitions. The main difference is they use
predicates instead of type checks.

I had to implement `>>=` operator as `>>` (right binary shift). There is also a
Python-specific `.get()` method to fetch an actual value from a monadic
instance. Be fair and use it only at the end of the monadic computation!

### Maybe

```python
# Define a monadic constructor
MaybeInt = f.maybe(f.p_int)

MaybeInt(2)
>>> Just[2]

MaybeInt("not an int")
>>> Nothing

# Monadic pipeline
MaybeInt(2) >> (lambda x: MaybeInt(x + 2))
>>> Just[4]

# Nothing breaks the pipeline
MaybeInt(2) >> (lambda x: f.Nothing()) >> (lambda x: MaybeInt(x + 2))
>>> Nothing
```

The better way to engage monads into you project is to use monadic decorators:

```python
@f.maybe_wraps(f.p_num)
def mdiv(a, b):
    if b:
        return a / b
    else:
        return None

mdiv(4, 2)
>>> Just[2]

mdiv(4, 0)
>>> Nothing
```

Use `.bind` method as an alias to `>>`:

```python

MaybeInt(2).bind(lambda x: MaybeInt(x + 1))
>>> Just[3]
```

You may pass additional arguments to both `.bind` and `>>` methods:

```python
MaybeInt(6) >> (mdiv, 2)
>>> Just[3]

MaybeInt(6).bind(mdiv, 2)
>>> Just[3]
```

Release the final value:

```python
m = MaybeInt(2) >> (lambda x: MaybeInt(x + 2))
m.get()
>>> 3
```

### Either

This monad presents two possible values: Left (negative) and Right
(positive).

```python
# create a constructor based on left and right predicates.
EitherStrNum = f.either(f.p_str, f.p_num)

EitherStrNum("error")
>>> Left[error]

EitherStrNum(42)
>>> Right[42]
```

Right value follows the pipeline, but Left breaks it.

```python
EitherStrNum(1) >> (lambda x: EitherStrNum(x + 1))
>>> Right[2]

EitherStrNum(1) >> (lambda x: EitherStrNum("error")) >> (lambda x: EitherStrNum(x + 1))
>>> Left[error]
```

When the plain value does not fit both predicates, `TypeError` occurs:

```python
EitherStrNum(None)
>>> TypeError: Value None doesn't fit...
```

Use decorator to wrap an existing function with Either logic:

```python
@f.either_wraps(f.p_str, f.p_num)
def ediv(a, b):
    if b == 0:
        return "Div by zero: %s / %s" % (a, b)
    else:
        return a / b


@f.either_wraps(f.p_str, f.p_num)
def esqrt(a):
    if a < 0:
        return "Negative number: %s" % a
    else:
        return math.sqrt(a)


EitherStrNum(16) >> (ediv, 4) >> esqrt
>>> Right[2.0]

EitherStrNum(16) >> (ediv, 0) >> esqrt
>>> Left[Div by zero: 16 / 0]
```

### IO

This monad wraps a function that does I/O operations. All the further calls
return monadic instances of the result.

```
IoPrompt = f.io(lambda prompt: raw_input(prompt))
IoPrompt("Your name: ")  # prompts for you name, I'll type "Ivan" and RET
>>> IO[Ivan]
```

Or use decorator:

```python
import sys

@f.io_wraps
def input(msg):
    return raw_input(msg)

@f.io_wraps
def write(text, chan):
    chan.write(text)

input("name: ") >> (write, sys.stdout)
>>> name: Ivan
>>> Ivan
>>> IO[None]
```

### Error

Error monad also known as `Try` in Scala is to prevent rising
exceptions. Instead, it provides `Success` sub-class to wrap positive result and
`Failture` to wrap an occured exception.

```
Error = f.error(lambda a, b: a / b)

Error(4, 2)
>>> Success[2]

Error(4, 0)
>>> Failture[integer division or modulo by zero]
```

Getting a value from `Failture` with `.get` method will re-rise it. Use
`.recover` method to deal with exception in a safe way.

```python
Error(4, 0).get()
ZeroDivisionError: integer division or modulo by zero

# value variant
Error(4, 0).recover(ZeroDivisionError, 42)
Success[2]
```

You may pass a tuple of exception classes. A value might be a function that
takes a exception instance and returns a proper value:

```python

def handler(e):
    logger.exception(e)
    return 0

Error(4, 0).recover((ZeroDivisionError, TypeError), handler)
>>> Success[0]
```

Decorator variant:

```python
@f.error_wraps
def tdiv(a, b):
    return a / b


@f.error_wraps
def tsqrt(a):
    return math.sqrt(a)

tdiv(16, 4) >> tsqrt
>>> Success[2.0]

tsqrt(16).bind(tdiv, 2)
>>> Success[2.0]
```

## Generics

Generic is a flexible callable object that may have different strategies
depending on a set of predicates (guards).

```python
# Create an instance
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
