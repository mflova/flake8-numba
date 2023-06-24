@guvectorize([], "() -> ()")
def func(val: int) -> None:
    val += 2
    return
