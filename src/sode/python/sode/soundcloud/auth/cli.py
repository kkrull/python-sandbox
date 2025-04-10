import logging
import os
from argparse import _SubParsersAction
from typing import Any

from sode.shared.cli import ProgramNamespace, RunState
from sode.shared.fp import Either, Left, Right

from .namespace import AuthNamespace

logger = logging.getLogger(__name__)


def add_auth(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str] = os.environ,
) -> None:
    """Add the auth sub-command"""

    AuthNamespace.add_command_subparser(subcommands, "auth", _run_auth, environ)


def fetch_tokens() -> Either[str, Any]:
    return Left("bang!")


# TODO KDK: Work here first to check for persisted, unexpired tokens or fetch and save them
def _run_auth(all_args: ProgramNamespace, state: RunState) -> int:
    cmd_args = AuthNamespace.upgrayedd(all_args)
    logger.debug({"soundcloud-auth": cmd_args.to_dict()})

    match fetch_tokens():
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case Right(_):
            return 0
