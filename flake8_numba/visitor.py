"""Module that implements the visitor logic.

This logic is in charge of executing specific code whenever some specific nodes within
the code are detected.
"""
import ast
import inspect
from functools import lru_cache
from typing import Final
from collections.abc import Sequence

from flake8_numba.rule import Rule
from flake8_numba.rules import nba2

_PREFIX: Final = "NBA"
"""Prefix used for defining all rules."""


@lru_cache
def _all_function_def_based_rules() -> Sequence[Rule]:
    members = inspect.getmembers(nba2)
    return [
        elem[1]  # type: ignore
        for elem in members
        if inspect.isclass(elem[1]) and _PREFIX in elem[1].__name__
    ]


class Visitor(ast.NodeVisitor):
    """Visitor class in charge of parsing one entire file."""

    def __init__(self) -> None:
        """Insantiate a list of empty errors just after being declared."""
        self.errors: list[tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        """Called whenever a function definition is found.

        Args:
            node (ast.FunctionDef): Node containing all the information relative to
                the function definition.
        """
        for rule in _all_function_def_based_rules():
            self.errors.extend(rule.check(node))
        self.generic_visit(node)
