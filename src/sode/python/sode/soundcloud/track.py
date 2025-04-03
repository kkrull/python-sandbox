import logging
from argparse import _SubParsersAction

from sode.shared.cli import factory
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.soundcloud.shared import SC_COMMAND

logger = logging.getLogger(__name__)


def add_track(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add the track sub-command"""

    track_parser = factory.add_command(
        subcommands,
        "track",
        command=_run_track,
        description="Work with tracks",
        help="hack tracks",
    )

    track_parser.add_argument(
        "--list",
        action="store_true",
        help="list tracks",
    )


def _run_track(args: ProgramNamespace, state: RunState) -> int:
    logger.debug(
        {
            "soundcloud-auth": {
                "args": args,
                "command": args.command,
                SC_COMMAND: getattr(args, SC_COMMAND),
                "list": args.list,
            }
        }
    )

    return 0
