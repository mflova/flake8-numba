@guvectorize([(int64[:], int64, int64[:]), (float64[:], float64[:])], '(n),()->(n)')
def g(x, y, res):
    ...