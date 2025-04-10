import logging
import os
from argparse import _SubParsersAction
from dataclasses import dataclass
from typing import Any

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from sode.shared.cli import ProgramNamespace, RunState
from sode.shared.fp import Either, Left, Right

from .namespace import AuthNamespace, ClientId, ClientSecret, TokenUrl

logger = logging.getLogger(__name__)


def add_auth(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str] = os.environ,
) -> None:
    """Add the auth sub-command"""

    AuthNamespace.add_command_subparser(subcommands, "auth", _run_auth, environ)


def _run_auth(all_args: ProgramNamespace, state: RunState) -> int:
    cmd_args = AuthNamespace.upgrayedd(all_args)
    logger.debug({"soundcloud-auth": cmd_args.to_dict()})
    match _run_auth_cmd(cmd_args, state):
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case Right(result):
            print(f"Done. result={result}", file=state.stderr)
            return 0


## auth module


@dataclass(frozen=True)
class TokenResponse:
    """How the SoundCloud OAuth2 token endpoint responds"""

    access_token: str
    expires_at: float  # 1743781923.9585016 // datetime.fromtimestamp
    expires_in: int  # 3599 // timedelta(seconds=)
    refresh_token: str
    scope: list[str]  # ['']
    token_type: str  # Bearer


def _auth_fetch_tokens(
    token_endpoint: TokenUrl, client_id: ClientId, client_secret: ClientSecret
) -> Either[str, TokenResponse]:
    """Request tokens from the specified OAuth2 endpoint using the client_credentials workflow.
    Return either tokens from a successful 2xx response or an error indicating a failed request."""

    logger.debug(
        {
            "fetch_tokens": {
                "client_id": client_id,
                "client_secret": client_secret,
                "token_endpoint": token_endpoint,
            }
        }
    )

    # https://developers.soundcloud.com/docs#authentication
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    try:
        return Right(oauth.fetch_token(auth=auth, token_url=token_endpoint)).map(
            lambda json_response: TokenResponse(**json_response)
        )
    except Exception as err:
        return Left(f"{token_endpoint}: {err}")


## This module


# TODO KDK: Work here first to check for persisted, unexpired tokens or fetch and save them
def _run_auth_cmd(args: AuthNamespace, _state: RunState) -> Either[str, TokenResponse]:
    return _fetch_tokens_ns(args)


def _fetch_tokens_ns(args: AuthNamespace) -> Either[str, TokenResponse]:
    match (args.token_endpoint_v, args.client_id_v, args.client_secret_v):
        case (Right(token_endpoint), Right(client_id), Right(client_secret)):
            return _auth_fetch_tokens(token_endpoint, client_id, client_secret)
        case lefts:
            return Left(next((l.left_value for l in lefts if l.is_left)))
