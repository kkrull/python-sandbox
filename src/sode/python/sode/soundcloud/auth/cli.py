import logging
import os
from argparse import _SubParsersAction

from sode.shared.cli import ProgramNamespace, RunState, argfactory, cmdfactory
from sode.soundcloud import SC_COMMAND

logger = logging.getLogger(__name__)


def add_auth(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str] = os.environ,
) -> None:
    """Add the auth sub-command"""

    auth_parser = cmdfactory.add_command(
        subcommands,
        "auth",
        command=_run_auth,
        description="Authorize with the SoundCloud API",
        help="authorize with SoundCloud API [start here]",
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        auth_parser.add_argument(
            "--client-id",
            **argfactory.environ_or_required("SOUNDCLOUD_CLIENT_ID", environ),
            help="OAuth2 client id with which to request access",
            nargs=1,
        ),
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        auth_parser.add_argument(
            "--client-secret",
            **argfactory.carrier_of_secrets(),
            **argfactory.environ_or_required("SOUNDCLOUD_CLIENT_SECRET", environ),
            nargs=1,
        ),
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        auth_parser.add_argument(
            "--token-endpoint",
            **argfactory.environ_or_default(
                "SOUNDCLOUD_TOKEN_URL",
                "https://secure.soundcloud.com/oauth/token",
                environ,
            ),
            help="URL to SoundCloud OAuth2 token endpoint (default: %(default)s)",
            metavar="URL",
            nargs=1,
        ),
    )


# TODO KDK: Work here to save the tokens
def _run_auth(args: ProgramNamespace, state: RunState) -> int:
    logger.debug(
        {
            "soundcloud-auth": {
                "command": args.command,
                SC_COMMAND: getattr(args, SC_COMMAND),
                "check_token_expiration": args.check_token_expiration,
                "client_id": args.client_id,
                "client_secret": args.client_secret,
            }
        }
    )

    return 0
