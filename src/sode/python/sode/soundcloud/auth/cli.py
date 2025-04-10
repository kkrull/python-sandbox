import logging
import os
from argparse import _SubParsersAction
from dataclasses import asdict

from sode.shared.cli import ProgramNamespace, RunState

from .namespace import AuthNamespace

logger = logging.getLogger(__name__)


def add_auth(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str] = os.environ,
) -> None:
    """Add the auth sub-command"""

    AuthNamespace.add_command_subparser(subcommands, "auth", _run_auth, environ)


# TODO KDK: Work here first to check for persisted, unexpired tokens or fetch and save them
def _run_auth(all_args: ProgramNamespace, state: RunState) -> int:
    cmd_args = AuthNamespace.upgrayedd(all_args)
    logger.debug({"soundcloud-auth": asdict(cmd_args)})

    return 0
