@guvectorize([(float32, float32), (int64,)], "() -> ()")
def func(val: int) -> None:
    ...
