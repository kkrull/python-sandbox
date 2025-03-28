import argparse
import pathlib

from sode.cli.option import BoolOption, regex_type
from sode.cli.state import MainState
from sode.shared.either import Either, Left, Right


class SodeNamespace(argparse.Namespace):
    debug: bool
    version: bool


def parse_args(state: MainState) -> Either[str, SodeNamespace]:
    parser = argparse.ArgumentParser(
        add_help=True,
        description="BRODE SODE: hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=state.program_name,
    )

    for option in _global_options:
        option.add_to(parser)

    sode_command_parsers = parser.add_subparsers(title="commands")
    fs_parser = sode_command_parsers.add_parser(
        "fs",
        description="sode fs: hack the local filesystem",
        help="hack the local file system",
    )

    fs_command_parsers = fs_parser.add_subparsers(title="sub-commands")
    fs_find_parser = fs_command_parsers.add_parser(
        "find",
        description="sode fs-find: find files in a filesystem",
        help="find files in a filesystem",
    )
    fs_find_parser.add_argument(
        "PATH",
        help="path in which to search",
        type=pathlib.Path,
    )
    fs_find_parser.add_argument(
        "PATTERN",
        help="pattern for which to search: ^.+$",
        type=regex_type(r"^.+$"),
    )

    try:
        return Right(parser.parse_args(args=state.arguments, namespace=SodeNamespace()))
    except argparse.ArgumentError as error:
        return Left(str(error))


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
