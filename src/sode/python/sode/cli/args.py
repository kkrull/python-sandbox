from argparse import ArgumentError, ArgumentParser, Namespace
from typing import Union

from sode.cli.state import MainState


class SodeNamespace(Namespace):
    debug: bool
    version: bool


def parse_args(state: MainState) -> Union[str, SodeNamespace]:
    parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE",
        exit_on_error=False,
        prog=state.program_name,
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="Log debugging output",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="Print version",
    )

    try:
        return parser.parse_args(args=state.arguments, namespace=SodeNamespace())
    except ArgumentError as error:
        return str(error)
