"""Module that implements the visitor logic.

This logic is in charge of executing specific code whenever some specific nodes within
the code are detected.
"""
import ast


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
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:  # noqa: N802
        """Called whenever a function returns a value.

        Args:
            node (ast.FunctionDef): Node containing all the information relative to
                the return value.
        """
        # print("Return value:", ast.dump(node.value))
        self.generic_visit(node)