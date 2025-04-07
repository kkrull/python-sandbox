import logging
from argparse import _SubParsersAction

import argcomplete

from sode.shared.cli import ProgramNamespace, RunState, add_command, argfactory
from sode.soundcloud import SC_COMMAND

logger = logging.getLogger(__name__)


def add_auth(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add the auth sub-command"""

    auth_parser = add_command(
        subcommands,
        "auth",
        command=_run_auth,
        description="Authorize with the SoundCloud API",
        help="authorize with SoundCloud API [start here]",
    )

    auth_parser.add_argument(
        "--check-token-expiration",
        action="store_true",
        help="check if persisted access token has expired",
    )

    argfactory.completable_argument(
        argcomplete.completers.ChoicesCompleter(choices=[]),  # type: ignore[no-untyped-call]
        auth_parser.add_argument(
            "--client-id",
            help="OAuth2 client id with which to request access",
            nargs="?",
        ),
    )

    argfactory.completable_argument(
        argcomplete.completers.ChoicesCompleter(choices=[]),  # type: ignore[no-untyped-call]
        auth_parser.add_argument(
            "--client-secret",
            help="OAuth2 client secret with which to request access",
            nargs="?",
        ),
    )


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
