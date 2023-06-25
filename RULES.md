# RULES

Current supported rules how to fix some of them can be seen below.

## NBA001

Raised when first positional argument has different inputs/outputs for the different
signatures provided.

```python
@vectorize([float64(float64, float64), (int64(int64))])  # ERROR
def f(...):
    ...
```

## NBA005

Raised when the first positional argument is not matching the function signature.

```python
@guvectorize([(float32, float32)], "() -> ()")
def func(val: float) -> int:  # ERROR (only one value)
    ...
```

## NBA006

Do not use `@vectorize` or `@guvectorize` for bound methods:

```python
class A:
    @guvectorize
    def method(self) -> None:
        ...
```

## NBA007

Expected X type for the first positional argument. Depending on the decorator you use,
message will differ:

- `@guvectorize`: Expects a list of tuples

```python
@guvectorize([float32, float32], "(n), (n) -> (n)")  # Error
def func(val1, val2, out):
    ...
```

- `@vectorize`: Expects a list

```python
@vectorize((float64(float64, float64))) # Error
def f(x, y):
    return x + y
```

## NBA101

Only one value can be returned with `@vectorize`:

```python
@vectorize([float64(float64, float64)])
def f(x, y):
    return x + y, 2  # Error
```

## NBA201

Raised when the number of input/outputs in the first positional argument is not matching
the number of input/outputs from second positional argument.

```python
# 3 values in 1st positional argument and 2 on the right side.
@guvectorize([(float32, float32, float32)], "() -> ()")
def func(...) -> None:
    ...
```

## NBA202

Raised when the sizes between the first and second positional arguments are not matching

```python
# 2nd argument is 1D at left but scalar on second positional argument
@guvectorize([(float32, float32[:], float32)], "(), () -> ()")
def func(...) -> None:
    ...
```

## NBA203

For the second signature, all those symbols that appear on the right side and not on the
left side are not properly defined.

```python
@guvectorize([(int64[:], int64, int64[:])], '(n),()->(m)')  # Error with `m`
def g(x, y, res):
    ...
```

(Solution)[https://github.com/numba/numba/issues/2797]: Pass a dummy array with the size
`m` to the input arguments so that `m` is defined for `numba`:

```python
@guvectorize([(int64[:], int64, int64[:])], '(n),(), (m)->(m)')  # OK
def g(x, y, dummy, res):
    ...
```

## NBA204

For the second signature, all those symbols must be non-constant (i.e any letter).

```python
@guvectorize([(int64[:], int64, int64[:])], '(n),(3)->()')  # Error with `3`
def g(x, y, res):
    ...
```

(Solution)[https://github.com/numba/numba/issues/2797]: Pass a dummy array with the
constant size `3` to the input arguments and change `3` by any other symbol

```python
# We define dummy to be ALWAYS an array of size 3. It will be represented by symbol k
# below.
@guvectorize([(int64[:], int64, int64[:])], '(n),(k)->()')  # OK
def g(x, y, dummy, res):
    ...
```

## NBA205

For `@guvectorize`, any `return` value is forbidden. It will have no effect and it will
confuse the developer. ## NBA206

```python
@guvectorize([(int64[:], int64, int64[:])], '(n),()->(n)')
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y
    return res  # Error
```

## NBA206

Raised when `@guvectorize` second positional argument has an open parenthesis.

```python
@guvectorize([(int64[:], int64, int64[:])], '(n),(->(n)')  # Error
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y
    return res  # Error
```

## NBA207

Raised when `@guvectorize` second positional argument is not a string.

```python
@guvectorize([(int64[:], int64, int64[:])], [float32, float64])  # Error
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y
    return res  # Error
```

## NBA208

`@guvectorize` needs to positional arguments:

```python
@guvectorize([(int64[:], int64, int64[:])])  # Error
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y
    return res  # Error
```

## NBA211

Raised when the second signature from `@guvectorize` is not suing commas to separate arrays:

```python
@guvectorize([(int64[:], int64, int64[:])], '(n)()->(n)')  # Error
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y
    return res  # Error
```