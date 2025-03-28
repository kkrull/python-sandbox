from argparse import ArgumentError, ArgumentParser, Namespace
from dataclasses import dataclass

from sode.cli.state import MainState
from sode.shared.either import Either, Left, Right


@dataclass
class BoolOption:
    help: str
    long_name: str
    short_name: str

    def add_to(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            self.short_name,
            self.long_name,
            action="store_true",
            default=False,
            help=self.help,
        )


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

    for option in global_options():
        option.add_to(parser)

    try:
        return Right(parser.parse_args(args=state.arguments, namespace=SodeNamespace()))
    except ArgumentError as error:
        return Left(str(error))


def global_options() -> list[BoolOption]:
    return [
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
