import argparse
import logging
import os
import textwrap
import typing
from argparse import RawTextHelpFormatter, _SubParsersAction
from typing import TypedDict

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from sode.shared.cli import argfactory, cmdfactory
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.shared.fp.either import Either, Left, Right
from sode.shared.fp.option import Empty, Option, Value
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

    match authorize(args):
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case Right(access_token):
            session = OAuth2Session(token={"access_token": access_token, "token_type": "Bearer"})

            # https://developers.soundcloud.com/docs/api/explorer/open-api#/users/get_users__user_id__playlists
            response = session.get(
                f"https://api.soundcloud.com/users/{args.user_id}/playlists",
                params={"limit": 1},
            )
            logger.debug(
                {
                    "headers": response.headers,
                    "links": response.links,
                    "status_code": response.status_code,
                },
            )

            print(response.text, file=state.stdout)
            return 0


class TokenResponse(TypedDict):
    access_token: str
    expires_at: float  # 1743781923.9585016
    expires_in: int  # 3599
    refresh_token: str
    scope: list[str]  # ['']
    token_type: str  # Bearer


def authorize(args: ProgramNamespace) -> Either[str, str]:
    match existing_access_token(args):
        case Value(access_token):
            return Right(access_token)
        case Empty():
            token_response = fetch_access_token(args)
            return token_response.map(lambda response: response["access_token"])


def existing_access_token(args: ProgramNamespace) -> Option[str]:
    access_token = args.access_token
    logger.debug({"existing_access_token": {"environ": access_token}})
    if access_token is None or len(access_token.strip()) == 0:
        return Empty[str]()
    else:
        return Value(access_token)


def fetch_access_token(args: ProgramNamespace) -> Either[str, TokenResponse]:
    client_id = args.client_id
    client_secret = args.client_secret
    token_url = args.token_endpoint

    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    # https://developers.soundcloud.com/docs#authentication
    try:
        auth_response: TokenResponse = typing.cast(
            TokenResponse,
            oauth.fetch_token(token_url=token_url, auth=auth),
        )
        logger.debug(
            {
                "fetch_access_token": {
                    "access_token": repr(auth_response["access_token"]),
                    "client_id": client_id,
                    "token_url": token_url,
                }
            }
        )

        access_token = (auth_response["access_token"] or "").strip()
        if len(access_token) == 0:
            return Left(f"missing access_token: {repr(auth_response)}")
        else:
            return Right(auth_response)
    except Exception as err:
        return Left(f"{token_url}: {err}")
