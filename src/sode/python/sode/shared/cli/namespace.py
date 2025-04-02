from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import Callable

from sode.shared.cli.state import RunState

type CliCommand = Callable[["ProgramNamespace", RunState], int]


class ProgramNamespace(Namespace):
    """Groups together parsed arguments and the indicated CLI command to run with them."""

    command: str
    debug: bool
    run_selected: CliCommand


def add_command_subparsers(
    main_parser: ArgumentParser,
) -> _SubParsersAction:  # type: ignore[type-arg]
    """Add an argument subparser group for commands to be added to the returned object"""
    return main_parser.add_subparsers(
        dest="command",
        metavar="COMMAND",
        required=True,
        title="commands",
    )


def add_global_arguments(parser: ArgumentParser, version: str) -> None:
    """Add global options that are used in this namespace."""

    parser.add_argument(
        "--debug",
        action="store_true",
        help="turn on the debug logger",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=version,
    )


def set_parser_command(parser: ArgumentParser, run_command: CliCommand) -> None:
    """Set the command that will run if this parser is activated."""

    parser.set_defaults(run_selected=run_command)
