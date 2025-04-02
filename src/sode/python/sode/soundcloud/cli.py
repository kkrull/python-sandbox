from argparse import _SubParsersAction

from sode.soundcloud.auth import add_auth
from sode.soundcloud.track import add_track


def add_soundcloud(
    command_parsers: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for the soundcloud commands"""
    sc_parser = command_parsers.add_parser(
        "soundcloud",
        description="Hack SoundCloud",
        help="hack SoundCloud",
    )
    sc_subcommands = sc_parser.add_subparsers(
        dest="command.soundcloud",
        metavar="SUBCOMMAND",
        title="subcommands",
    )

    add_auth(sc_subcommands)
    add_track(sc_subcommands)
