import argparse
import pathlib
import re
from typing import Any

from sode.cli.option import BoolOption, regex_type
from sode.cli.state import MainState
from sode.shared.either import Either, Left, Right


class FsFindNamespace(argparse.Namespace):
    path: pathlib.Path
    pattern: re.Pattern[str]


class SodeNamespace(argparse.Namespace):
    command: str
    fs_find: FsFindNamespace = FsFindNamespace()
    debug: bool
    version: bool


class FsFindAction(argparse.Action):
    def __call__(
        self,
        _parser: Any,
        namespace: argparse.Namespace,
        values: Any,
        _option_string: Any = None,
    ) -> None:
        dest = self.dest.lower()
        print(f"__call__: dest={dest}, values={values}")
        fs_find = getattr(namespace, "fs_find", FsFindNamespace())
        setattr(fs_find, dest, values)
        setattr(namespace, "fs_find", fs_find)


def parse_args(state: MainState) -> Either[str, SodeNamespace]:
    parser = argparse.ArgumentParser(
        add_help=True,
        description="BRODE SODE: hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=state.program_name,
    )

    for option in _global_options:
        option.add_to(parser)

    # Look here for inspiration: https://stackoverflow.com/questions/18668227/argparse-subcommands-with-nested-namespaces
    sode_parsers = parser.add_subparsers(
        dest="command",
        title="commands",
    )

    fs_find_parser = sode_parsers.add_parser(
        "fs-find",
        description="sode fs-find: find files in a filesystem",
        help="find files in a filesystem",
    )
    fs_find_parser.add_argument(
        "PATH",
        action=FsFindAction,
        default=argparse.SUPPRESS,
        help="path in which to search",
        type=pathlib.Path,
    )
    fs_find_parser.add_argument(
        "PATTERN",
        action=FsFindAction,
        default=argparse.SUPPRESS,
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
