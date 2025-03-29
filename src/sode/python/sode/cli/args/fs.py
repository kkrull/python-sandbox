import argparse
import pathlib
import re
from typing import Any, TypeVar

from sode.cli.shared.option import regex_type


def add_parser_to(
    parent: argparse._SubParsersAction,  # type: ignore[type-arg]
) -> None:
    fs_find_parser = parent.add_parser(
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


class FsFindNamespace(argparse.Namespace):
    path: pathlib.Path
    pattern: re.Pattern[str]


class FsNamespace(argparse.Namespace):
    find: FsFindNamespace


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
