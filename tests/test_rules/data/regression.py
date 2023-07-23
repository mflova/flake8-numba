"""Collection of correct functions that were triggered in the paste."""
from numba import void, float64, intp, f8, f4, int8, int16, int32, int64

@guvectorize([(float64[:], intp, float64[:])], '(n),()->(n)')
def move_mean(a, window_arr, out):
    out[:] = 2

@vectorize([f8(f8), f4(f4)])
def sinc(x):
    return 2

@vectorize("[f8(f8), f4(f4)]")
def sinc(x):
    return 2

@vectorize([int8(int8,int8),
            int16(int16,int16),
            int32(int32,int32),
            int64(int64,int64),
            f4(f4,f4),
            f8(f8,f8)])
def add(x,y):
    return 2

@guvectorize([void(int8,int8), void(f8,f8)], "() -> ()")
def add(x,y, out):
    out[:] = 2

@guvectorize("[void(int8,int8), void(f8,f8)]", "() -> ()")
def add(x,y, out):
    out[:] = 2

@vectorize([f8(f8), f4(f4)])
def logit(x):
    return 2

@vectorize([f8(f8),f4(f4)])
def expit(x):
    return 2