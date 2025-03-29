import argparse
from typing import Optional

from sode.cli.args.fs import FsArgs, add_fs_parser
from sode.cli.command import CliCommand
from sode.cli.shared.option import BoolOption
from sode.cli.state import MainState
from sode.shared.either import Either, Left, Right


class RootArgs(argparse.Namespace):
    command: str
    fs: Optional[FsArgs] = None
    debug: bool
    version: bool

    def to_command(self) -> Optional[CliCommand]:
        match self.fs:
            case FsArgs():
                return self.fs.to_command()
            case None:
                return None


def parse_args(state: MainState) -> Either[str, RootArgs]:
    parser = root_parser(state.program_name)
    try:
        return Right(parser.parse_args(args=state.arguments, namespace=RootArgs()))
    except argparse.ArgumentError as error:
        return Left(str(error))


def root_parser(program_name: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=True,
        description="BRODE SODE: hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=program_name,
    )

    for option in _global_options:
        option.add_to(parser)

    sode_parsers = parser.add_subparsers(dest="command", title="commands")
    add_fs_parser(sode_parsers)
    return parser


_global_options = [
    BoolOption(
        short_name="-d",
        long_name="--debug",
        help="log debugging output",
    ),
    BoolOption(
        short_name="-v",
        long_name="--version",
        help="print version",
    ),
]
