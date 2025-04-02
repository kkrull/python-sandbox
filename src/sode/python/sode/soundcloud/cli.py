from argparse import _SubParsersAction
from typing import Final

from sode.soundcloud.auth import add_auth
from sode.soundcloud.track import add_track

SC_COMMAND: Final[str] = "command.soundcloud"


def add_soundcloud(
    commands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for soundcloud commands"""
    sc_parser = commands.add_parser(
        "soundcloud",
        description="Hack SoundCloud",
        help="hack SoundCloud",
    )
    sc_subcommands = sc_parser.add_subparsers(
        dest=SC_COMMAND,
        metavar="SUBCOMMAND",
        title="subcommands",
    )

    add_auth(sc_subcommands)
    add_track(sc_subcommands)
