from argparse import ArgumentError, ArgumentParser, Namespace

from sode.cli.option import BoolOption
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

    for option in _global_options:
        option.add_to(parser)

    try:
        return Right(parser.parse_args(args=state.arguments, namespace=SodeNamespace()))
    except ArgumentError as error:
        return Left(str(error))


_global_options = [
    BoolOption(
        short_name="-d",
        long_name="--debug",
        help="Log debugging output",
    ),
    BoolOption(
        short_name="-v",
        long_name="--version",
        help="Print version",
    ),
]
