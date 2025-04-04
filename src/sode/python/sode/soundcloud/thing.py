import logging
import os
import typing
from argparse import _SubParsersAction
from pprint import pprint
from typing import TypedDict

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from sode.shared.cli import factory
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.shared.fp.either import Either, Left, Right
from sode.shared.fp.option import Empty, Option, Value
from sode.soundcloud.shared import SC_COMMAND

logger = logging.getLogger(__name__)


def add_the_thing(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a command that does "the thing" (anything) with SoundCloud"""

    thing_parser = factory.add_unlisted_command(
        subcommands,
        "thing",
        command=_run_thing,
        description="Do the thing (anything) with SoundCloud, to see if it works",
        epilog="""Find your API credentials at: https://soundcloud.com/you/apps""",
    )

    thing_parser.add_argument(
        "--client-id",
        default=os.environ["SOUNDCLOUD_CLIENT_ID"],
        help="OAuth2 client_id used for auth requests (optional, default: $SOUNDCLOUD_CLIENT_ID)",
        nargs="?",
    )


def _run_thing(args: ProgramNamespace, state: RunState) -> int:
    logger.debug(
        {
            "soundcloud-thing": {
                "client_id": args.client_id,
                "client_secret": os.environ["SOUNDCLOUD_CLIENT_SECRET"],
                "command": args.command,
                SC_COMMAND: getattr(args, SC_COMMAND),
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
                f"https://api.soundcloud.com/users/{os.environ["SOUNDCLOUD_USER_ID"]}/playlists",
                params={"limit": 1},
            )
            pprint(
                {
                    "content": response.content,
                    "headers": response.headers,
                    "links": response.links,
                    "status_code": response.status_code,
                },
                stream=state.stdout,
            )

            return 0


class TokenResponse(TypedDict):
    access_token: str
    # expires_at: float  # 1743781923.9585016
    # expires_in: int  # 3599
    # refresh_token: str
    # scope: list[str]  # ['']
    token_type: str  # Bearer


def authorize(args: ProgramNamespace) -> Either[str, str]:
    match existing_access_token(args):
        case Value(access_token):
            return Right(access_token)
        case Empty():
            token_response = fetch_access_token(args)
            return token_response.map(lambda response: response["access_token"])


def existing_access_token(args: ProgramNamespace) -> Option[str]:
    access_token = os.environ.get("SOUNDCLOUD_ACCESS_TOKEN", "")
    logger.debug({"existing_access_token": {"environ": access_token}})
    if len(access_token.strip()) == 0:
        return Empty[str]()
    else:
        return Value(access_token)


def fetch_access_token(args: ProgramNamespace) -> Either[str, TokenResponse]:
    client_id = args.client_id
    client_secret = os.environ["SOUNDCLOUD_CLIENT_SECRET"]
    token_url = os.environ["SOUNDCLOUD_TOKEN_URL"]

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
