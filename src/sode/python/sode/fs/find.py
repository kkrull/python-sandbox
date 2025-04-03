import logging
import textwrap
from argparse import _SubParsersAction
from pathlib import Path
from typing import Iterable

from sode.fs.shared import FS_COMMAND
from sode.shared.cli import namespace
from sode.shared.cli.format import DefaultsAndRawTextFormatter
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.shared.fp.option import Empty, Value


def add_find(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add the find sub-command"""

    find_parser = subcommands.add_parser(
        "find",
        description="Find files matching any of the specified criteria",
        epilog="""Example: %(prog)s --glob '**/index.[j,t]s' ~/git/node-sandbox ~/git/react""",
        formatter_class=DefaultsAndRawTextFormatter,
        help="find files lurking in the dark",
    )
    namespace.set_parser_command(find_parser, _run_find)

    find_parser.add_argument(
        "--exclude",
        action="extend",
        default=["**/.git/**", "**/node_modules/**"],
        help="path pattern(s) to exclude (repeatable)",
        metavar="GLOB",
        nargs=1,
    )
    find_parser.add_argument(
        "--glob",
        action="extend",
        help="path pattern(s) to match (repeatable)",
        metavar="GLOB",
        nargs=1,
    )
    find_parser.add_argument(
        "path",
        help=textwrap.dedent(
            f"""\
            path(s) in which to search for files
            (precede with -- to avoid ambiguity)
        """
        ),
        nargs="+",
    )


def _run_find(args: ProgramNamespace, state: RunState) -> int:
    logging.getLogger(__name__).debug(
        {
            "fs-find": {
                "command": args.command,
                FS_COMMAND: getattr(args, FS_COMMAND),
                "exclude": args.exclude,
                "glob": args.glob,
                "path": args.path,
            }
        }
    )

    for search_glob in args.glob:
        for search_root in [Path(p) for p in args.path]:
            for hit in [p for p in search_root.glob(search_glob) if not _excluded(p, args.exclude)]:
                print(hit, file=state.stdout)

    return 0


def _excluded(
    path: Path,
    exclude_patterns: Iterable[str],
) -> bool:
    matching_pattern = next(
        (Value(x) for x in exclude_patterns if path.full_match(x)),
        Empty[str](),
    )

    return matching_pattern.is_present
