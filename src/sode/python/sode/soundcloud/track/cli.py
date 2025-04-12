import logging
import textwrap
from argparse import RawTextHelpFormatter, _SubParsersAction

from sode.shared.cli import ProgramNamespace, RunState, cmdfactory

from ..namespace import SC_COMMAND
from . import list

logger = logging.getLogger(__name__)


def add_subcommand(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add the track sub-command"""

    track_parser = cmdfactory.add_command(
        subcommands,
        "track",
        command=_run_track,
        description=textwrap.dedent(
            """
        Work with tracks on SoundCloud.  Requires authorization with `auth`.
        """,
        ),
        formatter_class=RawTextHelpFormatter,
        help="hack tracks",
    )

    track_parser.add_argument(
        "--list",
        action="store_true",
        help="list tracks",
        required=True,
    )


def _run_track(args: ProgramNamespace, state: RunState) -> int:
    logger.debug(
        {
            "soundcloud-track": {
                "command": args.command,
                SC_COMMAND: getattr(args, SC_COMMAND),
                "list": args.list,
            }
        }
    )

    if args.list:
        return list.list_tracks(args, state)
    else:
        return 99
