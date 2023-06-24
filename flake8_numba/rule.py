"""Module that implement the logic that all rules will follow."""
import ast
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import NamedTuple, Optional, final


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

    @staticmethod
    @lru_cache
    def _check_rules_order(
        current_rule: str, skip_checks_if_these_errors_were_triggered: tuple[str, ...]
    ) -> None:
        """Check that current rule does not depend on future rules.

        Args:
            current_rule (str): Name of the current rule. Example: "NBA001"
            skip_checks_if_these_errors_were_triggered (tuple[str, ...]): All rules that
                need to be executed before `current_rule` is called.

        Raises:
            ValueError: _description_
        """
        all_rules_till_now = sorted(
            [current_rule, *skip_checks_if_these_errors_were_triggered]
        )
        if all_rules_till_now[-1] != current_rule:
            raise ValueError(
                f"{current_rule} depends on {all_rules_till_now[-1]} but this one will "
                "be executed later. Delete it from "
                "`skip_check_if_these_errors_were_triggered` or change the numbers, as "
                "they are executed in alpahebtical order."
            )

    @final
    def check(self, node: ast.FunctionDef, errors: list[Error]) -> None:
        """Check if the current rule is found to be broken within node.

        Args:
            node (ast.FunctionDef): Node describing the function definition.
            errors (list[Error]): Current list of errors founds. If new errors are found,
                they will be added to this list.
        """
        self._check_rules_order(
            type(self).__name__, self.skip_check_if_these_errors_were_triggered
        )
        if errors is None:
            errors = []
        for skip_if_error in self.skip_check_if_these_errors_were_triggered:
            for error in errors:
                if error.message.startswith(skip_if_error):
                    return
        new_error = self._check(node)
        if new_error:
            errors.append(new_error)
        return

    @abstractmethod
    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        """Given a node, find any possible issues.

        Args:
            node (ast.FunctionDef): Node that represents a small piece code.
        """
        ...

    @property
    def skip_check_if_these_errors_were_triggered(self) -> tuple[str, ...]:
        """Check will be automatically skip if these errors were triggered first.

        Meant to be overridden to add more rules.

        Be aware that the rules are called in alphabetical order.

        Returns:
            tuple[str, ...]: Tuple with all codes.
        """
        return ()
