import logging
import os
import textwrap
from argparse import RawTextHelpFormatter, _SubParsersAction
from pathlib import Path

from sode.shared.cli import ProgramNamespace, RunState, argfactory, cmdfactory
from sode.shared.state.path import default_state_dir

from ..namespace import SC_COMMAND
from . import list

logger = logging.getLogger(__name__)


def add_subcommand(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str],
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

    argfactory.completable_argument(
        argfactory.completion_choices(),
        track_parser.add_argument(
            "--state-dir",
            **argfactory.environ_or_default(
                "SODE_STATE",
                str(default_state_dir().absolute()),
                environ,
            ),
            help="Directory where sode stores its state data (default: %(default)s)",
            metavar="DIR",
            nargs=1,
        ),
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

    if not args.list:
        return 99

    list_state = list.ListTracksState(state_dir=Path(args.state_dir))
    return list.list_tracks(list_state)
