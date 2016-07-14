
### `f` library is a set of functional tools for Python

#### Functions

A bunch of useful functions to work with data structures.

- pcall

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
