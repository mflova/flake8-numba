"""Module that implement the logic that all rules will follow."""
import ast
from abc import ABC, abstractmethod
from typing import NamedTuple

from collections.abc import Sequence


class Error(NamedTuple):
    """Class that holds all the information relative to a single error."""

    line: int
    """Line where the error is located."""
    column: int
    """Column where the error is located."""
    message: str
    """Message of the error."""


class Rule(ABC):
    """Skeleton that all rules have to meet."""

    @classmethod
    @abstractmethod
    def check(cls, node: ast.FunctionDef) -> Sequence[Error]:
        """Given a node, find any possible issues.

        Args:
            node (ast.FunctionDef): Node that represents a small piece code.

        Returns:
            Sequence[Error]: Errors found. Empty if there were none.
        """
        ...
