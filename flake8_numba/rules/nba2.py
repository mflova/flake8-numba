import ast

from flake8_numba.rule import Error, Rule
from flake8_numba.utils import is_decorated_with, has_return_value

from collections.abc import Sequence


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
