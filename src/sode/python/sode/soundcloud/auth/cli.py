import logging
import os
from argparse import _SubParsersAction
from pathlib import Path

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
    match _run_auth_prepare(cmd_args).flat_map(lambda tup: _run_auth(*tup)):
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case Right(status):
            return status


def _run_auth_prepare(args: AuthNamespace) -> Either[str, tuple[Path, TokenResponse]]:
    return either.flatten_2_or_left(
        _ensure_user_file_exists(args.state_dir_v, "soundcloud-auth.json"),
        _fetch_tokens(args),
    )


def _run_auth(state_file_path: Path, tokens: TokenResponse) -> Either[str, int]:
    try:
        with open(state_file_path, mode="wt") as state_file:
            tokens.write_json(state_file, indent=2, sort_keys=True)
            return Right(0)
    except Exception as error:
        return Left(str(error))


def _ensure_user_file_exists(directory: Either[str, Path], filename: str) -> Either[str, Path]:
    return (
        directory.do_try(
            lambda exception: str(exception),
            lambda dir_path: dir_path.mkdir(0o700, exist_ok=True, parents=True),
        )
        .map(lambda dir_path: dir_path.joinpath(filename))
        .do_try(
            lambda exception: str(exception),
            lambda file_path: file_path.touch(0o600, exist_ok=True),
        )
    )


def _fetch_tokens(maybe_args: AuthNamespace) -> Either[str, TokenResponse]:
    return either.flatten_3_or_left(
        maybe_args.token_endpoint_v,
        maybe_args.client_id_v,
        maybe_args.client_secret_v,
    ).flat_map(lambda known_args: fetch_tokens(*known_args))
