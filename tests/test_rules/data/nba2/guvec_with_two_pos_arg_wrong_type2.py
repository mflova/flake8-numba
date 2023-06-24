@guvectorize([float32, float32], "() -> ()")
def func(val: int) -> None:
    val += 2
    return
