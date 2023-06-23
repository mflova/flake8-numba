import ast
from collections.abc import Iterable
from typing import NamedTuple, Union


class Location(NamedTuple):
    """Define the location for a given error."""

    line: int = 0
    column: int = 0


def is_decorated_with(
    decorator_names: Union[Iterable[str], str], node: ast.FunctionDef
) -> bool:
    decorator_names_ = (
        [decorator_names] if isinstance(decorator_names, str) else decorator_names
    )
    if node.decorator_list:
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                name = (
                    decorator.func.attr
                    if isinstance(decorator.func, ast.Attribute)
                    else decorator.func.id  # type: ignore
                )
            else:
                name = (
                    decorator.attr
                    if isinstance(decorator, ast.Attribute)
                    else decorator.id  # type: ignore
                )
            if name in decorator_names_:
                return True
    return False


def has_return_value(func_ast: ast.FunctionDef) -> tuple[bool, Location]:
    """Check if a given function has any return value.

    Args:
        func_ast (ast.FunctionDef): Function to be inspected.

    Returns:
        tuple[bool, Location]: Boolean value indicating whether there is and its
            corresponding location.
    """
    for node in ast.walk(func_ast):
        if isinstance(node, ast.Return) and node.value is not None:
            return True, Location(line=node.lineno, column=node.col_offset)
    return False, Location()
