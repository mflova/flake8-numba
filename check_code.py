"""Automated script to run all code quality related tools over the entire repo."""
import concurrent.futures
import multiprocessing
import os
import subprocess
import sys
from collections.abc import Iterable, Mapping
from typing import Any, Final, Optional

import click
import toml
import yaml
from colorama import Fore, Style, init

THIS_DIR: Final = os.path.dirname(__file__)
"""Absolute path to the folder holding this file."""
THIS_FILE: Final = os.path.basename(__file__)
"""Name of this file"""
TOML_FILE: Final = os.path.join(THIS_DIR, "pyproject.toml")
"""Absolute path to TOML file."""
ERR_MSG: Final = f"\n{Fore.LIGHTRED_EX}ERRORS WERE FOUND.{Style.RESET_ALL}"
"""Error message that will be displayed if something went wrong."""
OK_MSG: Final = f"\n{Fore.LIGHTGREEN_EX}EVERYTHING IS OK.{Style.RESET_ALL}"
"""Message that will be displayed if everything was ok."""

# Set up colorama
init(convert=True)

# Pre push hook
PRE_PUSH_TEMPLATE: Final = """#!/bin/sh

echo "\n"
echo "---------------RUNNING AUTOMATED TOOLS--------------------------"
cd "{cwd}"
python3 -m poetry run python "{file}"
if [ $? -eq 0 ]; then
  echo 'Everything is OK! Code will be pushed.'
  echo "-----------------------------------------------------------------\n"
  exit 0
else
  echo 'Errors found. Fix them, commit (or amend) the changes and try again.'
  echo "-----------------------------------------------------------------\n"
  exit 1
fi
"""


def print_output(
    command: str,
    *,
    status: bool,
    tool_desc: str = "",
    suggestions: Iterable[str] = "",
    err_str: str = "",
) -> None:
    """Pretty print the status or output returned from a linter.

    Args:
        command (str): Command used (typically name of the tool)
        status (bool): `True` if there were no problems. `False` otherwise.
        tool_desc (str, optional): Description of the tool that will be added to the
            message. Defaults to "".
        suggestions (Iterable[str], optional): Suggestions that will be printed if
            something went wrong.
        err_str (str, optional): Print the error string that was returned from the
            tool in case `status` is `False` (problems).
    """
    description = "" if not tool_desc else f" - {tool_desc}"
    if status is True:
        code = f"[{Fore.LIGHTGREEN_EX}OK{Style.RESET_ALL}]"
        print(f"{code} {command}{description}")
    else:
        # Put some indents
        err_lines = err_str.splitlines()
        prefix = "     "
        lines_with_prefix = [prefix + line for line in err_lines]
        err_str = "\n".join(lines_with_prefix)

        code = f"[{Fore.LIGHTRED_EX}NOK{Style.RESET_ALL}]"
        print(f"{code} {command}{description}")
        if suggestions:
            if isinstance(suggestions, str):
                print(f" - {Fore.LIGHTYELLOW_EX}{suggestions}{Style.RESET_ALL}")
            else:
                for suggestion in suggestions:
                    print(f" - {Fore.LIGHTYELLOW_EX}{suggestion}{Style.RESET_ALL}")
        print(f" - Output from the tool: \n{err_str}\n")


def run_tool(
    tool: str,
    *,
    extra_args: str = "",
    path: str = "",
    tool_desc: str = "",
    suggestions: Iterable[str] = "",
    ignore: Iterable[str] = "",
    only_include: Optional[Iterable[str]] = None,
    pass_if_output_contains: Iterable[str] = "",
) -> bool:
    """Run a linter-based tool.

    Args:
        tool (str): Name of the tool used. It will be used as command in CLI.
        extra_args (str, optional): Extra arguments passed to the tool.
        path (str, optional): Specific path that tool should analyze.
        tool_desc (str, optional): Description of the tool to be more verbose.
            Defaults to "".
        suggestions (Iterable[str], optional): Messages that will be displayed
            as suggestion in case something went wrong.
        ignore (Iterable[str], optional): All those lines from the output
            (stderr) of the tool containing these strings will be not printed.
        only_include (Optional[Iterable[str]], optional): Only those lines from
            the output (stderr) of the tool containing these strings will be
            printed.
        pass_if_output_contains (Iterable[str], optional): Return code will be
            modified from NOK to OK if otuput string contains any of these.

    Returns:
        bool: `True` if the tool succeeded.
    """
    if path:
        path = f'"{path}"'
    full_command = f"python3 -m poetry run {tool} {extra_args} {path}"
    process = subprocess.Popen(
        full_command,
        shell=True,
        cwd=THIS_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, err = process.communicate()  # Capture the output of tool execution
    output_str, err_str = output.decode("utf-8"), err.decode(
        "utf-8"
    )  # Decode the output to a string
    status = not bool(process.returncode) and "ERROR" not in output_str

    # Modify status if there are some specific keywords
    if pass_if_output_contains:
        for sub_str in pass_if_output_contains:
            if sub_str in output_str:
                status = True

    # For those tools that print errors into stdout instead of stderr, copy
    # problems into err_str
    if status is False:
        if output_str and not err_str:
            err_str = output_str

    # Filter output
    err_lines = err_str.split("\n")
    filtered_err_lines = [
        line for line in err_lines if not any([ignore_ in line for ignore_ in ignore])
    ]
    if only_include:
        filtered_err_lines = [
            line for line in err_lines if any([only_ in line for only_ in only_include])
        ]
    err_str = "\n".join(filtered_err_lines)

    print_output(
        tool,
        status=status,
        tool_desc=tool_desc,
        suggestions=suggestions,
        err_str=err_str,
    )
    if status is True:
        return True
    return False


def run_tool_from_dct(dct: Mapping[str, Any]) -> bool:
    """Wrapper around `run_tool` that forwards all arguments to `run_tool`.

    Typically used for multiprocessing purposes.

    Args:
        dct (Mapping[str, Any]): Arguments forwarded.
    """
    return run_tool(**dct)


def _disable_auto_run() -> None:
    """Disable git pre-push hook implemented by this same script."""
    pre_push_path = os.path.join(THIS_DIR, ".git", "hooks", "pre-push")
    if os.path.isfile(pre_push_path):
        os.remove(pre_push_path)
    print(
        f"{Fore.LIGHTGREEN_EX}Auto run removed!{Style.RESET_ALL} No code verification "
        "will be done before pushin to online repo."
    )


def _setup_auto_run() -> None:
    """Enable git pre-push hook to run this script before pushing."""
    pre_push_path = os.path.join(THIS_DIR, ".git", "hooks", "pre-push")
    if os.path.isfile(pre_push_path):
        print("An automatic auto-run of this script is already set up.")
        return

    with open(pre_push_path, "w") as f:
        f.write(PRE_PUSH_TEMPLATE.format(cwd=THIS_DIR, file=THIS_FILE))
    print(
        f"{Fore.LIGHTGREEN_EX}Auto run enabled!{Style.RESET_ALL} Whenever you push to the"
        " online repo, code will be first checked. To remove it, call this script with "
        "`--disable-auto-run."
    )


def read_and_parse_args(path: str = "") -> tuple[Mapping[str, Any], ...]:
    """Read and parse the yaml file indicating tools to be run.

    Args:
        path (str, optional): Path to the yaml file.

    Returns:
        tuple[Mapping[str, Any], ...]: Tuple being each element one call.
    """
    if not path:
        path = os.path.join(THIS_DIR, "check_code_args.yaml")
    with open(path) as f:
        all_args: list[dict[str, Any]] = yaml.load(f, Loader=yaml.SafeLoader)

    # Check format
    if not isinstance(all_args, list):
        raise ValueError("Configuration must be shaped as a list.")

    # Check mandatory args
    for args in all_args:
        if "tool" not in args:
            raise ValueError("At least the tool must be defined.")

    # Parse . to absolute current dir
    for args in all_args:
        if "path" in args and args["path"] == ".":
            args["path"] = THIS_DIR

    # Build pyanalyze arguments
    # This feature is not implemented on their side
    for args in all_args:
        if args["tool"] == "pyanalyze":
            if "extra_args" in args:
                raise ValueError("`extra_args` are not allowed for `pyanalyze`")

            if not os.path.isfile(TOML_FILE):
                raise ValueError(f"Could not find TOML file in {TOML_FILE}")

            with open(TOML_FILE) as f:
                content_toml = f.read()
            dct_toml = toml.loads(content_toml)

            extra_args: list[str] = ["--disable-all "]
            if "tool" in dct_toml and "pyanalyze" in dct_toml["tool"]:
                for arg, value in dct_toml["tool"]["pyanalyze"].items():
                    if isinstance(value, bool):
                        extra_args.append(f"--enable {arg} ")

            args["extra_args"] = "".join(extra_args)

    return tuple(all_args)


@click.command()
@click.option(
    "--auto-run",
    is_flag=True,
    help="Enable auto run whenever code is pushed to online repo.",
)
@click.option("--disable-auto-run", is_flag=True, help="Disable auto run.")
def main(auto_run: bool, disable_auto_run: bool) -> None:
    """Run all tools available.

    These are:

    - Linting tools: Ruff
    - Static type checker: Mypy
    - Testing tools: Pytest

    Args:
        auto_run (bool): `True` will make this script executable whenever you push
            to online repository.
        disable_auto_run (bool): `True` will disable the auto run mode created by
            the previous flag.

    Raises:
        ValueError: _description_
    """
    if auto_run and disable_auto_run:
        raise ValueError("Only one of the two flags can be set at the same time.")

    if disable_auto_run:
        _disable_auto_run()
        return
    if auto_run:
        _setup_auto_run()
        return

    results: list[bool] = []
    args = read_and_parse_args()
    num_workers = min(multiprocessing.cpu_count(), len(args))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(run_tool_from_dct, args_) for args_ in args]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    if False in results:
        print(ERR_MSG)
        sys.exit(1)
    print(OK_MSG)
    sys.exit(0)


if __name__ == "__main__":
    main()
