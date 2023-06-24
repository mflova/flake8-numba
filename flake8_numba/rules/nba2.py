import ast
from collections import Counter
from collections.abc import Sequence

from flake8_numba.rule import Error, Rule
from flake8_numba.utils import (
    get_decorator_n_args,
    get_pos_arg_from_decorator,
    has_return_value,
    is_decorated_with,
)


class NBA205(Rule):
    """Guvectorize function shall return None."""

    @classmethod
    def check(cls, node: ast.FunctionDef) -> Sequence[Error]:
        has_return, location = has_return_value(node)
        if has_return and is_decorated_with("guvectorize", node):
            msg = (
                "NBA205: Functions decorator with `@guvectorize` cannot return any value."
            )
            return [Error(location.line, location.column, msg)]
        return []


class NBA206(Rule):
    """When there are open parenthesis in second position argument signature."""

    @classmethod
    def check(cls, node: ast.FunctionDef) -> Sequence[Error]:
        if get_decorator_n_args(node, "args") != 2:
            return []
        signature, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(signature, str):
            return []
        counter = Counter(signature)
        print(counter)
        if counter["("] != counter[")"]:
            msg = "NBA206: Parenthesis on second positional argument are broken."
            return [Error(location.line, location.column, msg)]
        return []
