# Contributing

This repository uses `poetry` for the package and different tools to ensure code quality.
These are:

- Static type checkers: In order to ensure type safety, [mypy](https://mypy-lang.org/)
  and [pyanalyze](https://pyanalyze.readthedocs.io/en/latest/) (semi-static) are used.
- Spell checker: To fix basic typos,
  [codespell](https://github.com/codespell-project/codespell) is used.
- Linting: To ensure quality code is created, [ruff](https://beta.ruff.rs/docs/) is used.
  This tool groups main features provided by [pylint](https://pypi.org/project/pylint/)
  and [flake8](https://flake8.pycqa.org/en/latest/) but it is extremely fast and memory
  safe, as it is implemented in [rust](https://www.rust-lang.org/).
- Testing: To create easier to maintain code and bug free,
  [pytest](https://docs.pytest.org/en/7.3.x/) with
  [pytest-cov](https://pypi.org/project/pytest-cov/) and
  [pytest-deadfixtures](https://pypi.org/project/pytest-deadfixtures/) are used.
- Autoformatter: To ensure code is written in a homogeneous way among different
  developers, [black](https://github.com/psf/black) is being used.

These tools can be easily launched with:

```shell
poetry run python check_code.py
poetry run python check_code.py --auto-run  # Creates a pre-push hook
poetry run python check_code.py --disable-auto-run  # Disables pre-push hook
```

Or you can run them separately as:

```shell
poetry run pytest
poetry run black .
poetry run ruff .
poetry run codespell .
```