import logging
import os
from argparse import _SubParsersAction
from typing import Any

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


def fetch_tokens(
    token_endpoint: TokenUrl,
    client_id: ClientId,
    client_secret: ClientSecret,
) -> Either[str, Any]:
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

    return Right("fetched tokens...")


def _run_auth(all_args: ProgramNamespace, state: RunState) -> int:
    cmd_args = AuthNamespace.upgrayedd(all_args)
    logger.debug({"soundcloud-auth": cmd_args.to_dict()})
    match _run_auth_cmd(cmd_args, state):
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case Right(status):
            return status


# TODO KDK: Work here first to check for persisted, unexpired tokens or fetch and save them
def _run_auth_cmd(args: AuthNamespace, state: RunState) -> Either[str, int]:
    required = (args.token_endpoint_v, args.client_id_v, args.client_secret_v)
    match required:
        case (Right(token_endpoint), Right(client_id), Right(client_secret)):
            match fetch_tokens(token_endpoint, client_id, client_secret):
                case Left(err):
                    return Left(err)
                case Right(_):
                    return Right(0)
        case _:
            return Left(next((l.value for l in required if l.is_left)))
