from argparse import _SubParsersAction

from sode.shared.cli import add_subcommand_parsers

from . import FS_COMMAND
from .find import add_find


def add_fs(
    commands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for fs commands"""

    fs_parser = commands.add_parser(
        "fs",
        description="Hack a local filesystem",
        help="hack a local filesystem",
    )

    fs_subcommands = add_subcommand_parsers(fs_parser, FS_COMMAND)
    add_find(fs_subcommands)
