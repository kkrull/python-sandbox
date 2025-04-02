from argparse import _SubParsersAction

from sode.fs.find import add_find
from sode.fs.shared import FS_COMMAND


def add_fs(
    commands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for fs commands"""

    fs_parser = commands.add_parser(
        "fs",
        description="Hack a local filesystem",
        help="hack a local filesystem",
    )
    fs_subcommands = fs_parser.add_subparsers(
        dest=FS_COMMAND,
        metavar="SUBCOMMAND",
        title="subcommands",
    )

    add_find(fs_subcommands)
