import logging
import textwrap
from argparse import _SubParsersAction
from pathlib import Path
from typing import Iterable

import argcomplete

from sode.fs import FS_COMMAND
from sode.shared.cli import DefaultsAndRawTextFormatter, ProgramNamespace, RunState, cmdfactory
from sode.shared.fp import Empty, Value

logger = logging.getLogger(__name__)


def add_find(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add the find sub-command"""

    find_parser = cmdfactory.add_command(
        subcommands,
        "find",
        command=_run_find,
        description="Find files matching any of the specified criteria",
        epilog="""Example: %(prog)s --glob '**/index.[j,t]s' ~/git/node-sandbox ~/git/react""",
        formatter_class=DefaultsAndRawTextFormatter,
        help="find files lurking in the dark",
    )

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
    ).completer = argcomplete.completers.ChoicesCompleter(  # type: ignore[attr-defined, no-untyped-call]
        choices=[]
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
    ).completer = argcomplete.completers.DirectoriesCompleter()  # type: ignore[attr-defined, no-untyped-call]


def _run_find(args: ProgramNamespace, state: RunState) -> int:
    logger.debug(
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
