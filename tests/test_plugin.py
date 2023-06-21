import ast

import pytest

from flake8_numba import Plugin


class TestPlugin:
    """Tests for the Plugin class."""

    @pytest.fixture
    def code_sample(self) -> ast.Module:
        """Instance of `ast.Module` that represents an arbitrary code sample."""
        code = """
def hello_world() -> None:
    print("Hello World")
        """
        return ast.parse(code)

    def test_plugin(self, code_sample: ast.Module) -> None:
        """Test that the plugin can be instantiated properly.

        Args:
            code_sample (ast.Module): Code sample with no issues.
        """
        plugin = Plugin(code_sample)
        plugin.run()
