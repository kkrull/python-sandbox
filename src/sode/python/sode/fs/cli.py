from argparse import _SubParsersAction
from pprint import pprint

from sode.shared.cli import namespace
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState


def add_fs(
    command_parsers: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for the fs commands"""

    fs_parser = command_parsers.add_parser(
        "fs",
        description="Hack a local filesystem",
        help="hack a local filesystem",
    )
    fs_subcommands = fs_parser.add_subparsers(
        dest="command.fs",
        metavar="SUBCOMMAND",
        title="subcommands",
    )

    _find_add(fs_subcommands)


def _find_add(
    fs_subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    find_parser = fs_subcommands.add_parser(
        "find",
        description="Find files lurking in the dark",
        help="find files",
    )
    namespace.set_parser_command(find_parser, _find_run)

    find_parser.add_argument(
        "--name",
        help="pattern to match filenames",
        metavar="PATTERN",
        nargs=1,
    )
    find_parser.add_argument(
        "path",
        help="path(s) in which to search for files",
        nargs="+",
    )


def _find_run(args: ProgramNamespace, state: RunState) -> int:
    pprint(
        {
            "fs-find": {
                "args": args,
                "command": args.command,
                "command.fs": getattr(args, "command.fs"),
                "debug": args.debug,
                "name": args.name,
                "path": args.path,
            }
        },
        stream=state.stdout,
    )

    return 0
