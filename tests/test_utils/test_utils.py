from flake8_numba import utils
from numba import float32
import ast
import pytest
import os
from typing import Optional


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


class TestDecoratorHasArguments:
    @pytest.mark.parametrize(
        "relative_path, decorator_has_arguments",
        [
            ("data/decorator_has_arguments/func_with_decorator_and_arguments", True),
            ("data/decorator_has_arguments/func_with_decorator", False),
            ("data/decorator_has_arguments/func_with_no_decorator", False),
        ],
    )
    def test_decorator_has_arguments(
        self, relative_path: str, decorator_has_arguments: bool, node: ast.FunctionDef
    ) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            relative_path (str): Relative path where the function is located.
            decorator_has_arguments (bool): Expected output of the function to be tested.
            node (ast.FunctionDef): Node representing the function stored in `relative_path`
        """
        assert decorator_has_arguments == utils.decorator_has_arguments(node)


class TestGetDecoratorNArgs:
    @pytest.mark.parametrize(
        "relative_path, n_positional_args_in_decorator",
        [
            ("data/get_decorator_n_args/func_with_no_decorator", 0),
            ("data/get_decorator_n_args/func_with_decorator", 0),
            ("data/get_decorator_n_args/func_with_decorator_and_parenthesis", 0),
            ("data/get_decorator_n_args/func_with_2_pos_args", 2),
            ("data/get_decorator_n_args/func_with_2_pos_args_and_kwargs", 2),
            ("data/get_decorator_n_args/func_with_one_var_as_pos_arg", 1),
            ("data/get_decorator_n_args/func_with_one_list_as_pos_arg", 1),
        ],
    )
    def test_get_n_positional_args_decorator(
        self,
        relative_path: str,
        n_positional_args_in_decorator: bool,
        node: ast.FunctionDef,
    ) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            relative_path (str): Relative path where the function is located.
            n_positional_args_in_decorator (int): Number of positional arguments defined
                in decorator at `relative_path`
            node (ast.FunctionDef): Node representing the function stored in `relative_path`
        """
        assert n_positional_args_in_decorator == utils.get_decorator_n_args(
            node, arg_type="args"
        )

    @pytest.mark.parametrize(
        "relative_path, n_kwargs_in_decorator",
        [
            ("data/get_decorator_n_args/func_with_no_decorator", 0),
            ("data/get_decorator_n_args/func_with_decorator", 0),
            ("data/get_decorator_n_args/func_with_decorator_and_parenthesis", 0),
            ("data/get_decorator_n_args/func_with_2_kwargs", 2),
            ("data/get_decorator_n_args/func_with_2_kwargs_and_args", 2),
        ],
    )
    def test_get_n_kwargs_decorator(
        self, relative_path: str, n_kwargs_in_decorator: bool, node: ast.FunctionDef
    ) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            relative_path (str): Relative path where the function is located.
            n_positional_args_in_decorator (int): Number of positional arguments defined
                in decorator at `relative_path`
            node (ast.FunctionDef): Node representing the function stored in `relative_path`
        """
        assert n_kwargs_in_decorator == utils.get_decorator_n_args(
            node, arg_type="kwargs"
        )

    @pytest.mark.parametrize(
        "relative_path, n_args_in_decorator",
        [
            ("data/get_decorator_n_args/func_with_2_kwargs_and_args", 3),
        ],
    )
    def test_get_n_args_decorator(
        self, relative_path: str, n_args_in_decorator: bool, node: ast.FunctionDef
    ) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            relative_path (str): Relative path where the function is located.
            n_positional_args_in_decorator (int): Number of positional arguments defined
                in decorator at `relative_path`
            node (ast.FunctionDef): Node representing the function stored in `relative_path`
        """
        assert n_args_in_decorator == utils.get_decorator_n_args(node)


class TestGetPosArgFromDecorator:
    @pytest.mark.parametrize(
        "relative_path, at, returned_value",
        [
            ("data/get_pos_arg_from_decorator/func_with_no_decorator", 0, None),
            ("data/get_pos_arg_from_decorator/func_with_no_decorator", 1, None),
            ("data/get_pos_arg_from_decorator/func_with_dec_and_parenthesis", 0, None),
            ("data/get_pos_arg_from_decorator/func_with_dec_and_parenthesis", 1, None),
            ("data/get_pos_arg_from_decorator/func_with_one_pos_arg", 0, "[a, b]"),
            ("data/get_pos_arg_from_decorator/func_with_one_pos_arg", 1, None),
            ("data/get_pos_arg_from_decorator/func_with_two_pos_args", 0, "value1"),
            ("data/get_pos_arg_from_decorator/func_with_two_pos_args", 1, "value2"),
            ("data/get_pos_arg_from_decorator/func_with_only_kwargs", 0, None),
            ("data/get_pos_arg_from_decorator/func_with_only_kwargs", 1, None),
            (
                "data/get_pos_arg_from_decorator/func_with_mixed_symbols",
                0,
                "[float32(float32, value3)]",
            ),
            (
                "data/get_pos_arg_from_decorator/func_with_numba_types",
                0,
                [float32(float32, float32)],
            ),
        ],
    )
    def test_get_n_args_decorator(
        self,
        relative_path: str,
        returned_value: Optional[object],
        at: int,
        node: ast.FunctionDef,
    ) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            relative_path (str): Relative path where the function is located.
            at (int): Index of the positional argument that should be returned.
            returned_value (Optional[object]): Expected returned value from the function.
            node (ast.FunctionDef): Node representing the function stored in `relative_path`
        """
        assert returned_value == utils.get_pos_arg_from_decorator(at, node)[0]
