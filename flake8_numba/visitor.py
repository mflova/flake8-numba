"""Module that implements the visitor logic.

This logic is in charge of executing specific code whenever some specific nodes within
the code are detected.
"""
import ast
import inspect
from collections.abc import Sequence
from functools import lru_cache
from typing import Any

from flake8_numba.rule import Error, Rule
from flake8_numba.rules import nba0, nba1, nba2


@lru_cache
def _all_rules() -> Sequence[Rule]:
    class_list = []
    members: list[Any] = []
    members.extend(inspect.getmembers(nba0))
    members.extend(inspect.getmembers(nba1))
    members.extend(inspect.getmembers(nba2))
    # Obtener todos los miembros del módulo
    for _, obj in members:
        # Verificar si el miembro es una clase
        if inspect.isclass(obj) and issubclass(obj, Rule) and obj != Rule:
            class_list.append(obj())
    return class_list


class Visitor(ast.NodeVisitor):
    """Visitor class in charge of parsing one entire file."""

    def __init__(self) -> None:
        """Insantiate a list of empty errors just after being declared."""
        self.errors: list[Error] = []
        self.pending_rules: set[Rule] = set(_all_rules())
        self.rules_raised: set[type[Rule]] = set()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        """Called whenever a function definition is found.

        Args:
            node (ast.FunctionDef): Node containing all the information relative to
                the function definition.
        """
        for rule in _all_rules():
            self.process_rule(rule, node)
        self.generic_visit(node)

    def process_rule(self, rule: Rule, node: ast.FunctionDef) -> None:
        # Process dependencies
        if rule.depends_on:
            for pre_rule in rule.depends_on:
                self.process_rule(pre_rule(), node)
        # Process rules with dependencies solved
        if rule in self.pending_rules:
            # Skip if the rule that depends on was already raised.
            if self.rules_raised & rule.depends_on:
                return
            # Rules are appended internally within .check
            is_ok = rule.check(node, self.errors)
            if not is_ok:
                self.rules_raised.add(type(rule))
            self.pending_rules.remove(rule)
