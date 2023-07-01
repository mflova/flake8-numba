@guvectorize([(float32[:], float32[:]), (int64[:], int64[:])], "(n) -> (n)")
def func(val, output) -> None:
    output[0] = 1
