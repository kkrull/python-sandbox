import argparse
import pathlib
import re
from argparse import Action, ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Any, Optional, override

from sode.cli.command import CliCommand, RunState
from sode.cli.shared.option import regex_type
from sode.shared.attr import ensure_attr


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
    def __call__(self, p: ArgumentParser, root: Namespace, values: Any, _opt: Any = None) -> None:
        dest = self.dest.lower()
        fs = ensure_attr(root, "fs", FsArgs())
        find = ensure_attr(fs, "find", FindArgs())
        setattr(find, dest, values)


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
    find: Optional[FindArgs] = None

    def to_command(self) -> Optional[CliCommand]:
        match self.find:
            case FindArgs():
                return FsCommand(self)
            case None:
                return None


@dataclass
class FsCommand(CliCommand):
    args: FsArgs

    @override
    def run(self, state: RunState) -> int:
        print(f"FsCommand: args={self.args}", file=state.stdout)
        return 0
