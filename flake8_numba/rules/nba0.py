import ast
from collections.abc import Sequence

from flake8_numba.rule import Error, Rule
from flake8_numba.utils import (
    get_decorator_location,
    get_decorator_n_args,
    get_pos_arg_from_decorator,
    is_decorated_with,
)


class NBA007(Rule):
    """Expected X type for first positional argument."""

    @classmethod
    def check(cls, node: ast.FunctionDef) -> Sequence[Error]:
        if not is_decorated_with(["guvectorize", "vectorize"], node):
            return []

        if get_decorator_n_args(node, "args") == 0:
            return []

        first_arg, location = get_pos_arg_from_decorator(0, node)
        if is_decorated_with("guvectorize", node):
            msg = (
                "NBA207: Expected a list of tuples. Each one containing a valid "
                "signature of the type `(*input_types, *rtypes)`."
            )
            if not isinstance(first_arg, list):
                return [Error(location.line, location.column, msg)]
            for signature in first_arg:
                if not isinstance(signature, tuple):
                    return [Error(location.line, location.column, msg)]
            return []
        if is_decorated_with("vectorize", node):
            msg = (
                "NBA207: Expected a list with each element being `rtype(*input_types)` "
                "with numba types."
            )
            if not isinstance(first_arg, list):
                return [Error(location.line, location.column, msg)]
            return []
        return []


class NBA006(Rule):
    """Do not use decorator for bound methods."""

    @classmethod
    def check(cls, node: ast.FunctionDef) -> Sequence[Error]:
        if not is_decorated_with(["guvectorize", "vectorize"], node):
            return []

        parameters = node.args.args
        if parameters:
            first_parameter = parameters[0]
            first_variable_name = first_parameter.arg
        if first_variable_name in ("cls", "self"):
            msg = "NBA206: Cannot use this decorator in bound methods."
            location = get_decorator_location(["vectorize", "guvectorize"], node)
            return [Error(location.line, location.column, msg)]  # type: ignore

        return []