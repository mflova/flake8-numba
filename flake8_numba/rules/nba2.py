import ast
import re
from collections import Counter
from typing import Any, Optional, cast

from flake8_numba.rule import Error, Rule
from flake8_numba.rules import nba0
from flake8_numba.utils import (
    Location,
    get_decorator_location,
    get_decorator_n_args,
    get_pos_arg_from_decorator,
    has_return_value,
    is_decorated_with,
)


class NBA201(Rule):
    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        first_arg, _ = get_pos_arg_from_decorator(0, node)
        second_arg, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(second_arg, str) or not isinstance(first_arg, list):
            return None
        len_second_arg = Counter(second_arg)["("]

        for idx, signature in enumerate(first_arg):
            if len(signature) != len_second_arg:
                msg = (
                    f"NBA201: Number of inputs/outputs in {idx} signature is not "
                    "matching the one provided in the second argument."
                )
                return Error(location.line, location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {nba0.NBA007, NBA203, NBA204}  # First two positional arguments are ok


class NBA202(Rule):
    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        first_arg, _ = get_pos_arg_from_decorator(0, node)
        first_arg = cast(list[tuple[Any, ...]], first_arg)
        second_arg, location = get_pos_arg_from_decorator(1, node)
        second_arg = cast(str, second_arg)

        # Get sizes from second positional argument
        pattern = r"\(((?:[a-zA-Z]+(?:,\s*[a-zA-Z]+)*)?)\)"
        sizes_from_second_arg: list[int] = []
        symbol: str
        for match in re.findall(pattern, second_arg):
            count = 0
            for symbol in match:
                if symbol.isalpha():
                    count += 1
            sizes_from_second_arg.append(count)

        sizes_from_first_arg: list[int] = []
        for signature in first_arg:
            sizes_from_first_arg = []
            for value in signature:
                if hasattr(value, "ndim"):
                    sizes_from_first_arg.append(value.ndim)
                else:
                    sizes_from_first_arg.append(0)
            if sizes_from_first_arg != sizes_from_second_arg:
                msg = (
                    f"NBA202: Sizes between first signature ({sizes_from_first_arg}) "
                    f"and second positional argument ({sizes_from_second_arg}) are "
                    "not matching."
                )
                return Error(location.line, location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {nba0.NBA007, NBA203, NBA204}  # First two positional arguments are ok


class NBA203(Rule):
    """Undefined symbol in second positional argument."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        signature, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(signature, str):
            return None
        count = Counter(signature)
        if "->" not in signature or count[")"] < 2 or count["("] < 2 or count["-"] > 1:
            return None

        inputs, outputs = signature.split("->")
        diff = set(outputs) - set(inputs)
        for elem in diff:
            if elem.isalpha():
                msg = f"NBA203: Symbol `{elem}` must be also defined on the left side."
                return Error(location.line, location.column, msg)

        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA206, NBA207, NBA208}  # 2 args, no open parenthesis + second pos is str


class NBA204(Rule):
    """Constants are not allowed in second positional argument."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        signature, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(signature, str):
            return None
        count = Counter(signature)
        if "->" not in signature or count[")"] < 2 or count["("] < 2 or count["-"] > 1:
            return None

        for elem in signature:
            if elem.isdigit():
                msg = (
                    f"NBA204: Constants (`{elem}`) are not allowed in the second "
                    "signature."
                )
                return Error(location.line, location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA206, NBA207, NBA208}  # 2 args, no open parenthesis + second pos is str


class NBA205(Rule):
    """Guvectorize function shall return None."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        has_return, location = has_return_value(node)
        if has_return and is_decorated_with("guvectorize", node):
            msg = (
                "NBA205: Functions decorator with `@guvectorize` cannot return any value."
            )
            return Error(location.line, location.column, msg)
        return None


class NBA206(Rule):
    """Open parenthesis in second position argument signature."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if not is_decorated_with("guvectorize", node):
            return None
        if get_decorator_n_args(node, "args") != 2:
            return None
        signature, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(signature, str):
            return None
        counter = Counter(signature)
        if counter["("] != counter[")"]:
            msg = "NBA206: Parenthesis on second positional argument are broken."
            return Error(location.line, location.column, msg)
        return None


class NBA207(Rule):
    """Second argument must define the sizes-related signature (string type)."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if (
            not is_decorated_with("guvectorize", node)
            or get_decorator_n_args(node, "args") != 2
        ):
            return None
        signature, location = get_pos_arg_from_decorator(1, node)
        if signature is None:
            return None

        msg = (
            "NBA206: A second signature (str type) must be provided with "
            "corresponding sizes of inputs and outputs."
        )
        if not isinstance(signature, str):  # If numba based signature
            return Error(location.line, location.column, msg)
        counter = Counter(signature)
        if counter["("] < 2 or counter[")"] < 2 or "->" not in signature:
            return Error(location.line, location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA208}


class NBA208(Rule):
    """Guvectorize needs two positional arguments."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if is_decorated_with("guvectorize", node):
            first_arg = get_pos_arg_from_decorator(0, node)

            msg = (
                "NBA208: Guvectorize strictly needs two positional arguments: list "
                "of tuples and string"
            )
            location = get_decorator_location("guvectorize", node)
            location = cast(Location, location)
            if get_decorator_n_args(node, "args") != 2:
                return Error(location.line, location.column, msg)
            if isinstance(first_arg[0], list):
                if len(first_arg[0]) == 0:
                    return Error(location.line, location.column, msg)
                for elem in first_arg[0]:
                    if not isinstance(elem, tuple):
                        return Error(location.line, location.column, msg)
                return None
            return Error(location.line, location.column, msg)
        return None
