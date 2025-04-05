import argparse
import logging
import os
import textwrap
from argparse import RawTextHelpFormatter, _SubParsersAction
from typing import Any, Mapping, NewType

from oauthlib.oauth2 import BackendApplicationClient
from requests import Response
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from sode.shared.cli import argfactory, cmdfactory
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.shared.fp.either import Either, Left, Right
from sode.shared.fp.option import Empty, Option, Value
from sode.soundcloud.shared import SC_COMMAND

logger = logging.getLogger(__name__)

## OAuth2


class AccessToken:
    value: str
    token_type: str

    def __init__(self, value: str, token_type: str):
        self.value = value
        self.token_type = token_type

    @staticmethod
    def expected(value: str, token_type: str) -> Either[str, "AccessToken"]:
        if len(token_type.strip()) == 0:
            return Left(f"unknown token_type: {repr(token_type)}")

        match value:
            case str(value) if len(value.strip()) > 0:
                return Right(AccessToken(value.strip(), token_type.strip()))
            case str(value):
                return Left(f"empty value: {repr(value)}")
            case None:
                return Left(f"missing value: {repr(value)}")
            case _ as value:
                return Left(f"unknown type of value: {repr(value)}")

    @staticmethod
    def maybe(value: str, token_type: str = "Bearer") -> Option["AccessToken"]:
        match value:
            case None:
                return Empty[AccessToken]()
            case str(_) if len(value.strip()) == 0:
                return Empty[AccessToken]()
            case str(v):
                return Value(AccessToken(v.strip(), token_type.strip()))

    def oauth_session(self) -> OAuth2Session:
        return OAuth2Session(token={"access_token": self.value, "token_type": self.token_type})


class TokenResponse:
    _mapping: dict[str, Any]
    # access_token: str
    # expires_at: float  # 1743781923.9585016
    # expires_in: int  # 3599
    # refresh_token: str
    # scope: list[str]  # ['']
    # token_type: str  # Bearer

    def __init__(self, raw_response: Mapping[str, Any]):
        self._mapping = dict(raw_response)

    @staticmethod
    def of(raw_response: Mapping[str, Any]) -> "TokenResponse":
        return TokenResponse(raw_response)

    @property
    def access_token(self) -> Either[str, AccessToken]:
        return AccessToken.expected(self._mapping["access_token"], self._mapping["token_type"])


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
            response = one_playlist(args, access_token)
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


def one_playlist(args: ProgramNamespace, access_token: AccessToken) -> Response:
    # https://developers.soundcloud.com/docs/api/explorer/open-api
    session = access_token.oauth_session()
    return session.get(
        f"https://api.soundcloud.com/users/{args.user_id}/playlists",
        params={"limit": 1},
    )


def authorize(args: ProgramNamespace) -> Either[str, AccessToken]:
    match existing_access_token(args):
        case Value(access_token):
            return Right(access_token)
        case Empty():
            return fetch_tokens(args).flat_map(lambda response: response.access_token)


def existing_access_token(args: ProgramNamespace) -> Option[AccessToken]:
    logger.debug({"existing_access_token": {"environ": repr(args.access_token)}})
    return AccessToken.maybe(args.access_token, "Bearer")


def fetch_tokens(args: ProgramNamespace) -> Either[str, TokenResponse]:
    """Authorize with the client_credentials workflow"""

    logger.debug(
        {
            "fetch_tokens": {
                "client_id": repr(args.client_id),
                "token_url": repr(args.token_endpoint),
            }
        }
    )

    # https://developers.soundcloud.com/docs#authentication
    auth = HTTPBasicAuth(args.client_id, args.client_secret)
    client = BackendApplicationClient(client_id=args.client_id)
    oauth = OAuth2Session(client=client)

    try:
        return Right(oauth.fetch_token(auth=auth, token_url=args.token_endpoint)).map(
            lambda x: TokenResponse.of(x)
        )
    except Exception as err:
        return Left(f"{args.token_endpoint}: {err}")
