from flake8_numba import utils
import ast
import pytest
import os


@pytest.fixture
def node(relative_path: str) -> ast.FunctionDef:
    """Node of type FunctionDef.

    In order to work in tests, user must define `relative_path` fixture. This is a
    relative path to the function to be loaded and exported as a node.

    Args:
        relative_path (str): Relative path where the function is located.

    Returns:
        ast.FunctionDef: Representation of the function as node.
    """
    abs_path = os.path.join(os.path.dirname(__file__), relative_path + ".py")
    with open(abs_path) as f:
        function = f.read()
    return ast.parse(function).body[0]  # type: ignore


class TestHasReturnValue:
    @pytest.mark.parametrize(
        "relative_path, has_return_value",
        [
            ("data/has_return_value/func_with_no_return", False),
            ("data/has_return_value/func_with_return_none", False),
            ("data/has_return_value/func_with_return", True),
        ],
    )
    def test_has_return_value(
        self, relative_path: str, has_return_value: bool, node: ast.FunctionDef
    ) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            relative_path (str): Relative path where the function is located.
            has_return_value (bool): Expected output of the function.
            node (ast.FunctionDef): Node representing the function stored in `relative_path`
        """
        assert has_return_value == utils.has_return_value(node)[0]


class TestIsDecoratedWith:
    @pytest.mark.parametrize(
        "relative_path, is_decorated_with_guvec",
        [
            ("data/is_decorated_with/func_with_guvec", True),
            ("data/is_decorated_with/func_with_numba_guvec", True),
            ("data/is_decorated_with/func_with_nb_guvec", True),
            ("data/is_decorated_with/func_with_vec", False),
            ("data/is_decorated_with/non_decorated_func", False),
        ],
    )
    def test_is_decorated_with(
        self, relative_path: str, is_decorated_with_guvec: bool, node: ast.FunctionDef
    ) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            relative_path (str): Relative path where the function is located.
            is_decorated_with_guvec(bool): Expected output of the function to be tested.
            node (ast.FunctionDef): Node representing the function stored in `relative_path`
        """
        assert is_decorated_with_guvec == utils.is_decorated_with("guvectorize", node)
