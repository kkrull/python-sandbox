import logging
import os
from argparse import _SubParsersAction
from pathlib import Path
from typing import assert_never

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

    AuthNamespace.add_command_subparser(subcommands, "auth", _run_auth_shell, environ)


def _run_auth_shell(all_args: ProgramNamespace, state: RunState) -> int:
    cmd_args = AuthNamespace.upgrayedd(all_args)
    logger.debug({"soundcloud-auth": cmd_args.to_dict()})
    match _run_auth_core(cmd_args, state):
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case Right(result):
            print(f"Done. result={result}", file=state.stderr)
            return 0


def _run_auth_core(args: AuthNamespace, _state: RunState) -> Either[str, int]:
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

    return either.flatten_2_or_left(
        _ensure_user_file(args.state_dir_v, "soundcloud-auth.json"),
        _fetch_tokens(args),
    ).flat_map(lambda x: _run_auth_finally(x))


def _ensure_user_file(dir: Either[str, Path], filename: str) -> Either[str, Path]:
    return (
        dir.do_try(
            lambda exception: str(exception),
            lambda state_dir: state_dir.mkdir(0o700, parents=True, exist_ok=True),
        )
        .map(lambda dir: dir.joinpath(filename))
        .do_try(
            lambda exception: str(exception),
            lambda file_path: file_path.touch(0o600, exist_ok=True),
        )
    )


def _fetch_tokens(args: AuthNamespace) -> Either[str, TokenResponse]:
    return either.flatten_3_or_left(
        args.token_endpoint_v,
        args.client_id_v,
        args.client_secret_v,
    ).flat_map(lambda arg: fetch_tokens(arg[0], arg[1], arg[2]))


def _run_auth_finally(values: tuple[Path, TokenResponse]) -> Either[str, int]:
    try:
        with open(values[0], mode="wt") as state_file:
            values[1].write_json(state_file, indent=2, sort_keys=True)
            return Right(0)
    except Exception as error:
        return Left(str(error))
