import ast

import pytest

from flake8_numba.visitor import Visitor


class TestVisitor:
    """Test class Visitor."""

    @pytest.fixture
    def code_sample(self) -> ast.Module:
        """Instance of `ast.Module` that represents an arbitrary code sample."""
        code = """
def hello_world() -> None:
    print("Hello World")
        """
        return ast.parse(code)

    def test_visitor(self, code_sample: ast.Module) -> None:
        """Test that the visitor can traverse code without breaking anything.

        Args:
            code_sample (ast.Module): Code sample with no issues.
        """
        visitor = Visitor()
        visitor.visit(code_sample)
