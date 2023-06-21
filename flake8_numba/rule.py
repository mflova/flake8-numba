"""Module that implement the logic that all rules will follow."""
import ast
from abc import ABC, abstractclassmethod
from typing import NamedTuple

from typing_extensions import Self


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
    
    @abstractclassmethod
    def check(self: Self, node: ast) -> list[Error]:  # type: ignore
        """Given a node, find any possible issues.

        Args:
            node (ast): Node that represents a small piece code.

        Returns:
            list[Error]: Errors found. Empty if there were none.
        """
        ...