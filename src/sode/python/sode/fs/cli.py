import os
from argparse import _SubParsersAction

from sode.shared.cli import add_subcommand_parsers

from . import find
from .namespace import FS_COMMAND


def add_command(
    commands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str],
) -> None:
    """Add a parser for fs commands"""

    fs_parser = commands.add_parser(
        "fs",
        description="Hack a local filesystem",
        help="hack a local filesystem",
    )

    fs_subcommands = add_subcommand_parsers(fs_parser, FS_COMMAND)
    find.add_subcommand(fs_subcommands, environ)
