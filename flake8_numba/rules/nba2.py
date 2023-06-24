import ast
from collections import Counter
from collections.abc import Sequence
from typing import cast

from flake8_numba.rule import Error, Rule
from flake8_numba.utils import (
    Location,
    get_decorator_location,
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
        if not is_decorated_with("guvectorize", node):
            return []
        if get_decorator_n_args(node, "args") != 2:
            return []
        signature, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(signature, str):
            return []
        counter = Counter(signature)
        if counter["("] != counter[")"]:
            msg = "NBA206: Parenthesis on second positional argument are broken."
            return [Error(location.line, location.column, msg)]
        return []


class NBA207(Rule):
    """Second argument must define the sizes-related signature (string type)."""

    @classmethod
    def check(cls, node: ast.FunctionDef) -> Sequence[Error]:
        if (
            not is_decorated_with("guvectorize", node)
            or get_decorator_n_args(node, "args") != 2
        ):
            return []
        signature, location = get_pos_arg_from_decorator(1, node)
        if signature is None:
            return []

        msg = (
            "NBA206: A second signature (str type) must be provided with "
            "corresponding sizes of inputs and outputs."
        )
        if not isinstance(signature, str):  # If numba based signature
            return [Error(location.line, location.column, msg)]
        counter = Counter(signature)
        if counter["("] < 2 or counter[")"] < 2 or "->" not in signature:
            return [Error(location.line, location.column, msg)]
        return []


class NBA208(Rule):
    """Guvectorize needs two positional arguments."""

    @classmethod
    def check(cls, node: ast.FunctionDef) -> Sequence[Error]:
        if is_decorated_with("guvectorize", node):
            first_arg = get_pos_arg_from_decorator(0, node)

            msg = (
                "NBA208: Guvectorize strictly needs two positional arguments: list "
                "of tuples and string"
            )
            location = get_decorator_location("guvectorize", node)
            location = cast(Location, location)
            if get_decorator_n_args(node, "args") != 2:
                return [Error(location.line, location.column, msg)]
            if isinstance(first_arg[0], list):
                if len(first_arg[0]) == 0:
                    return [Error(location.line, location.column, msg)]
                for elem in first_arg[0]:
                    if not isinstance(elem, tuple):
                        return [Error(location.line, location.column, msg)]
                return []
            return [Error(location.line, location.column, msg)]
        return []
