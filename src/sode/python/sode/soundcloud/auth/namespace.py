import os
import textwrap
from argparse import RawTextHelpFormatter, _SubParsersAction
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, NewType

from sode.shared.cli import CliCommand, ProgramNamespace, argfactory, cmdfactory
from sode.shared.fp import Either, new_option
from sode.shared.state.path import default_state_dir

from ..namespace import SC_COMMAND

ClientId = NewType("ClientId", str)
ClientSecret = NewType("ClientSecret", str)
TokenUrl = NewType("TokenUrl", str)


@dataclass
class AuthNamespace(ProgramNamespace):
    """Argument namespace for the auth command"""

    client_id: str
    client_secret: str
    state_dir: str
    token_endpoint: str

    @staticmethod
    def add_command_subparser(
        subcommands: _SubParsersAction,  # type: ignore[type-arg]
        name: str,
        command: CliCommand,
        environ: os._Environ[str],
    ) -> None:
        """
        Add a sub-parser with the given name to run the given command, upon activation.

        The returned sub-parser is capable of parsing the arguments in this namespace from
        command-line arguments and environment variables (e.g. for defaults and overrides) from the
        given environment.
        """

        auth_parser = cmdfactory.add_command(
            subcommands,
            name,
            command=command,
            description=textwrap.dedent(
                """
            (Re-)authorize with the SoundCloud API, saving tokens for later use with other commands.

            environment variables:
              Safely avoid passing secrets on the command line:
                SOUNDCLOUD_CLIENT_ID      override --client-id with a secret
                SOUNDCLOUD_CLIENT_SECRET  override --client-secret with a secret

              Override defaults or CLI arguments:
                SOUNDCLOUD_TOKEN_URL      override --token-endpoint
                SOUNDCLOUD_USER_ID        override --user-id
            """,
            ),
            epilog="Find your API credentials at: https://soundcloud.com/you/apps",
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
                    str(default_state_dir().absolute()),
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

    @staticmethod
    def upgrayedd(args: ProgramNamespace) -> "AuthNamespace":
        """Upgrade base namespace with this command's fields for a double-dose of parsing power"""

        all_args = dict(args._get_kwargs())
        useful_args = {arg: value for arg, value in all_args.items() if arg not in [SC_COMMAND]}
        return AuthNamespace(**useful_args)

    @property
    def client_id_v(self) -> Either[str, ClientId]:
        """either the typed, non-empty client ID, or an error"""

        return (
            new_option(self.client_id)
            .map(lambda x: x.strip())
            .filter(lambda x: len(x) > 0)
            .map(lambda x: ClientId(x))
            .to_right("client_id: missing or empty")
        )

    @property
    def client_secret_v(self) -> Either[str, ClientSecret]:
        """either the typed, non-empty client secret, or an error"""

        return (
            new_option(self.client_secret)
            .map(lambda x: x.strip())
            .filter(lambda x: len(x) > 0)
            .map(lambda x: ClientSecret(x))
            .to_right("client_secret: missing or empty")
        )

    @property
    def state_dir_v(self) -> Either[str, Path]:
        return (
            new_option(self.state_dir)
            .map(lambda x: x.strip())
            .filter(lambda x: len(x) > 0)
            .map(lambda x: Path(x))
            .to_right("state_dir: missing or empty")
        )

    @property
    def token_endpoint_v(self) -> Either[str, TokenUrl]:
        """either the typed, non-empty token endpoint, or an error"""

        return (
            new_option(self.token_endpoint)
            .map(lambda x: x.strip())
            .filter(lambda x: len(x) > 0)
            .map(lambda x: TokenUrl(x))
            .to_right("token_endpoint: missing or empty")
        )

    def to_dict(self) -> dict[str, Any]:
        """each argument's name and value, as a dictionary"""

        return asdict(self)
