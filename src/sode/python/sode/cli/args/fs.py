import argparse
import pathlib
import re
from argparse import Action, ArgumentParser, Namespace
from typing import Any

from sode.cli.shared.option import regex_type


def _add_find_parser(
    parent: argparse._SubParsersAction,  # type: ignore[type-arg]
) -> None:
    find_parser: argparse.ArgumentParser = parent.add_parser(
        "find",
        description="sode fs find: find files in the ether",
        help="find files in the ether",
    )
    find_parser.add_argument(
        "PATH",
        action=FindAction,
        default=argparse.SUPPRESS,
        help="path in which to search",
        type=pathlib.Path,
    )
    find_parser.add_argument(
        "PATTERN",
        action=FindAction,
        default=argparse.SUPPRESS,
        help="pattern for which to search",
        type=regex_type(r"^.+$"),
    )


class FindAction(Action):
    def __call__(
        self, parser: ArgumentParser, root: Namespace, values: Any, _options: Any = None
    ) -> None:
        dest = self.dest.lower()
        print(f"__call__: dest={dest}, namespace={root}, parser={parser.prog}, values={values}")
        fs = getattr(root, "fs", FsArgs())
        find = getattr(fs, "find", FindArgs())
        setattr(find, dest, values)
        setattr(fs, "find", find)
        setattr(root, "fs", fs)


class FindArgs(Namespace):
    path: pathlib.Path
    pattern: re.Pattern[str]


def add_fs_parser(
    parent: argparse._SubParsersAction,  # type: ignore[type-arg]
) -> None:
    fs_parser: argparse.ArgumentParser = parent.add_parser(
        "fs",
        description="sode fs: hack the local filesystem",
        help="hack the local filesystem",
    )

    subcommand_parsers = fs_parser.add_subparsers(title="sub-commands")
    _add_find_parser(subcommand_parsers)


class FsArgs(Namespace):
    find: FindArgs
