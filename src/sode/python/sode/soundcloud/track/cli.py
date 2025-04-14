import logging
import os
import textwrap
from argparse import RawTextHelpFormatter, _SubParsersAction
from pathlib import Path

from sode.shared.cli import ProgramNamespace, RunState, argfactory, cmdfactory
from sode.shared.fp.either import Either, Left
from sode.shared.oauth.token import AccessToken
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

        environment variables:
          Override defaults or CLI arguments:
            SOUNDCLOUD_USER_ID        override --user-id
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
            **argfactory.optional_with_default(str(default_state_dir().absolute())),
            help="Directory where sode stores its state data (default: %(default)s)",
            metavar="DIR",
            nargs=1,
        ),
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        track_parser.add_argument(
            "-u",
            "--user-id",
            **argfactory.environ_or_required("SOUNDCLOUD_USER_ID", environ),
            help="SoundCloud user ID",
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

    list_state = list.ListTracksState(
        access_token=lambda: load_access_token(args.state_dir),
        stderr=state.stderr,
        stdout=state.stdout,
        user_id=args.user_id,
    )
    return list.list_tracks(list_state)


def load_access_token(state_dir: Path) -> Either[str, AccessToken]:
    return Left("load_access_token: not implemented")
