import ast
from collections.abc import Iterable
from typing import Literal, NamedTuple, Union, overload


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


def decorator_has_arguments(node: ast.FunctionDef) -> bool:
    """Check whether a function has a decortor with arguments.

    Args:
        node (ast.FunctionDef): Node representing the function definition.

    Returns:
        bool: `True` if the function is decorated AND it uses arguments. `False`
            otherwise.
    """
    if not node.decorator_list:
        return False

    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call) and decorator.args:
            return True

    return False


@overload
def get_decorator_n_args(node: ast.FunctionDef, arg_type: Literal["args"]) -> int:
    ...


@overload
def get_decorator_n_args(node: ast.FunctionDef, arg_type: Literal["kwargs"]) -> int:
    ...


@overload
def get_decorator_n_args(node: ast.FunctionDef, arg_type: Literal[""] = "") -> int:
    ...


def get_decorator_n_args(node: ast.FunctionDef, arg_type: str = "") -> int:
    """Get number of arguments in decorator.

    Args:
        node (ast.FunctionDef): Node representing the function definition.
        arg_type (Union[Literal["kwargs"],Literal["args"],Literal[""]]): Specify which
            arguments are counted. Positional, kwargs or both. Both by default.

    Returns:
        int: Count of positional arguments for the decorator.
    """
    if not node.decorator_list:
        return 0

    args_count: int = 0
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call) and decorator.args:
            if arg_type in ("args", ""):
                for arg in decorator.args:
                    if isinstance(arg, (ast.Name, ast.Constant)):
                        args_count += 1
        if isinstance(decorator, ast.Call) and decorator.keywords:
            if arg_type in ("kwargs", ""):
                for keyword in decorator.keywords:
                    if isinstance(keyword, ast.keyword):
                        args_count += 1
    return args_count
