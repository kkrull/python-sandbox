import logging
import os
import textwrap
from argparse import RawTextHelpFormatter, _SubParsersAction
from dataclasses import asdict, dataclass
from pathlib import Path

from sode.shared.cli import ProgramNamespace, RunState, argfactory, cmdfactory
from sode.soundcloud import SC_COMMAND

logger = logging.getLogger(__name__)


def add_auth(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str] = os.environ,
) -> None:
    """Add the auth sub-command"""

    auth_parser = cmdfactory.add_command(
        subcommands,
        "auth",
        command=_run_auth,
        description=textwrap.dedent(
            """
        (Re-)authorize with the SoundCloud API.  Save tokens for later use with other commands.

        environment variables:
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
        help="(re-)authorize with SoundCloud API [start here]",
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        auth_parser.add_argument(
            "--client-id",
            **argfactory.environ_or_required("SOUNDCLOUD_CLIENT_ID", environ),
            help="OAuth2 client id with which to request access",
            nargs=1,
        ),
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        auth_parser.add_argument(
            "--client-secret",
            **argfactory.carrier_of_secrets(),
            **argfactory.environ_or_required("SOUNDCLOUD_CLIENT_SECRET", environ),
            nargs=1,
        ),
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        auth_parser.add_argument(
            "--state-dir",
            **argfactory.environ_or_default(
                "SODE_STATE",
                str(_sode_default_state_dir().absolute()),
                environ,
            ),
            help="Directory where sode stores its state data (default: %(default)s)",
            metavar="DIR",
            nargs=1,
        ),
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        auth_parser.add_argument(
            "--token-endpoint",
            **argfactory.environ_or_default(
                "SOUNDCLOUD_TOKEN_URL",
                "https://secure.soundcloud.com/oauth/token",
                environ,
            ),
            help="URL to SoundCloud OAuth2 token endpoint (default: %(default)s)",
            metavar="URL",
            nargs=1,
        ),
    )


def _sode_default_state_dir() -> Path:
    return Path.home().joinpath(".local", "state", "sode")


@dataclass
class AuthNamespace(ProgramNamespace):
    """Argument namespace for the auth command"""

    # TODO KDK: Can these be typed?
    client_id: str
    client_secret: str
    state_dir: str
    token_endpoint: str

    @staticmethod
    def upgrayedd(args: ProgramNamespace) -> "AuthNamespace":
        """Upgrade argument namespace for a double-dose of parsing power"""

        all_args = dict(args._get_kwargs())
        useful_args = {arg: value for arg, value in all_args.items() if arg not in [SC_COMMAND]}
        return AuthNamespace(**useful_args)


# TODO KDK: Work here first to check for persisted, unexpired tokens or fetch and save them
def _run_auth(all_args: ProgramNamespace, state: RunState) -> int:
    cmd_args = AuthNamespace.upgrayedd(all_args)
    logger.debug({"soundcloud-auth": asdict(cmd_args)})

    return 0
