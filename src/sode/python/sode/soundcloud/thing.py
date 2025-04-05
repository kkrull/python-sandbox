import argparse
import logging
import os
import textwrap
from argparse import RawTextHelpFormatter, _SubParsersAction

from sode.shared.cli import argfactory, cmdfactory
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.shared.fp.either import Either, Left, Right
from sode.shared.fp.option import Empty, Option, Value
from sode.shared.oauth.token import AccessToken
from sode.soundcloud import playlist
from sode.soundcloud.authapi import scauth_fetch_tokens
from sode.soundcloud.shared import SC_COMMAND

logger = logging.getLogger(__name__)


def add_the_thing(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str] = os.environ,
) -> None:
    """Add a command that "does the thing" (literally anything) with SoundCloud"""

    thing_parser = cmdfactory.add_unlisted_command(
        subcommands,
        "thing",
        command=_run_thing,
        description=textwrap.dedent(
            """
        Zhu Li, Do the Thing!
        In other words, check if anything works with SoundCloud.

        environment variables:
          To use existing authorization:
            SOUNDCLOUD_ACCESS_TOKEN   use an existing token instead of requesting one

          Safely avoid passing secrets on the command line:
            SOUNDCLOUD_CLIENT_ID      override --client-id with a secret
            SOUNDCLOUD_CLIENT_SECRET  override --client-secret with a secret

          Override defaults or CLI arguments:
            SOUNDCLOUD_TOKEN_URL      override --token-endpoint
            SOUNDCLOUD_USER_ID        override --user-id

        Find your API credentials at: https://soundcloud.com/you/apps
        """,
        ),
        formatter_class=RawTextHelpFormatter,
    )
    thing_parser.add_argument(
        "--access-token",
        **argfactory.environ_or_optional("SOUNDCLOUD_ACCESS_TOKEN", environ),
        help=argparse.SUPPRESS,  # discourage exposing secret CLI arguments to other users
        nargs=1,
    )
    thing_parser.add_argument(
        "--client-id",
        **argfactory.environ_or_required("SOUNDCLOUD_CLIENT_ID", environ),
        help="OAuth2 client_id used to request tokens (default: $SOUNDCLOUD_CLIENT_ID)",
        nargs=1,
    )
    thing_parser.add_argument(
        "--client-secret",
        **argfactory.environ_or_required("SOUNDCLOUD_CLIENT_SECRET", environ),
        help=argparse.SUPPRESS,  # discourage exposing secret CLI arguments to other users
        nargs=1,
    )
    thing_parser.add_argument(
        "--token-endpoint",
        **argfactory.environ_or_default(
            "SOUNDCLOUD_TOKEN_URL",
            "https://secure.soundcloud.com/oauth/token",
            environ,
        ),
        help="URL to SoundCloud OAuth2 token endpoint (default: %(default)s)",
        metavar="URL",
        nargs=1,
    )
    thing_parser.add_argument(
        "-u",
        "--user-id",
        **argfactory.environ_or_required("SOUNDCLOUD_USER_ID", environ),
        help="SoundCloud user ID",
        nargs=1,
    )


def _run_thing(args: ProgramNamespace, state: RunState) -> int:
    logger.debug(
        {
            "soundcloud-thing": {
                "access_token": args.access_token,
                "client_id": args.client_id,
                "client_secret": args.client_secret,
                "command": args.command,
                SC_COMMAND: getattr(args, SC_COMMAND),
                "token_endpoint": args.token_endpoint,
                "user_id": args.user_id,
            }
        }
    )

    match scauth_authorize(args):
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case Right(access_token):
            response = playlist.any(args.user_id, access_token)
            logger.debug(
                {
                    "_run_thing": {
                        "request_headers": response.request.headers,
                        "status_code": response.status_code,
                    }
                },
            )

            print(response.text, file=state.stdout)
            return 0


## OAuth 2


def sodeenv_existing_access_token(args: ProgramNamespace) -> Option[AccessToken]:
    logger.debug({"existing_access_token": repr(args.access_token)})
    return AccessToken.maybe(args.access_token, "Bearer")


## SoundCloud auth


def scauth_authorize(args: ProgramNamespace) -> Either[str, AccessToken]:
    match sodeenv_existing_access_token(args):
        case Value(access_token):
            return Right(access_token)
        case Empty():
            return scauth_fetch_tokens(
                args.token_endpoint,
                client_id=args.client_id,
                client_secret=args.client_secret,
            ).flat_map(lambda response: response.access_token)
