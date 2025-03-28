from argparse import ArgumentError, ArgumentParser, Namespace

from sode.cli.state import MainState
from sode.shared.either import Either, Left, Right


class SodeNamespace(Namespace):
    debug: bool
    version: bool


def parse_args(state: MainState) -> Either[str, SodeNamespace]:
    parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE",
        exit_on_error=False,
        prog=state.program_name,
    )

    add_global_options(parser)
    try:
        return Right(parser.parse_args(args=state.arguments, namespace=SodeNamespace()))
    except ArgumentError as error:
        return Left(str(error))


def add_global_options(parser: ArgumentParser) -> None:
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
