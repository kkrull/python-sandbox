import logging
import os
from argparse import _SubParsersAction

from sode.shared.cli import ProgramNamespace, RunState
from sode.shared.fp import Either, Left, Right, either
from sode.soundcloud.auth.api import TokenResponse, fetch_tokens

from .namespace import AuthNamespace

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


## This module


def _run_auth_cmd(args: AuthNamespace, _state: RunState) -> Either[str, int]:
    logger.debug(
        {
            "_run_auth_cmd": {
                "client_id_v": args.client_id_v,
                "client_secret_v": args.client_secret_v,
                "state_dir_v": args.state_dir_v,
                "token_endpoint_v": args.token_endpoint_v,
            }
        },
    )

    match args.state_dir_v.do_try(
        lambda exception: str(exception),
        lambda state_dir: state_dir.mkdir(0o700, parents=True, exist_ok=True),
    ):
        case Left(state_dir_error):
            return Left(state_dir_error)

    auth_state_path = args.state_dir_v.map(lambda dir: dir.joinpath("soundcloud-auth.json"))
    match auth_state_path.do_try(
        lambda exception: str(exception),
        lambda file_path: file_path.touch(0o600, exist_ok=True),
    ):
        case Left(state_dir_error):
            return Left(state_dir_error)

    match _fetch_tokens_ns(args):
        case Left(fetch_error):
            return Left(fetch_error)
        case Right(tokens):
            with open(auth_state_path.right_value, mode="wt") as state_file:
                tokens.write_json(state_file, indent=2, sort_keys=True)
                return Right(0)


def _fetch_tokens_ns(maybe_args: AuthNamespace) -> Either[str, TokenResponse]:
    return either.flatten_3_or_left(
        maybe_args.token_endpoint_v, maybe_args.client_id_v, maybe_args.client_secret_v
    ).flat_map(lambda arg: fetch_tokens(arg[0], arg[1], arg[2]))
