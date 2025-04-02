from argparse import _SubParsersAction
from pprint import pprint

from sode.fs.shared import FS_COMMAND
from sode.shared.cli import namespace
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState


def add_find(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add the find sub-command"""

    find_parser = subcommands.add_parser(
        "find",
        description="Find files lurking in the dark",
        help="find files",
    )
    namespace.set_parser_command(find_parser, _run_find)

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


def _run_find(args: ProgramNamespace, state: RunState) -> int:
    pprint(
        {
            "fs-find": {
                "args": args,
                "command": args.command,
                FS_COMMAND: getattr(args, FS_COMMAND),
                "debug": args.debug,
                "name": args.name,
                "path": args.path,
            }
        },
        stream=state.stdout,
    )

    return 0
