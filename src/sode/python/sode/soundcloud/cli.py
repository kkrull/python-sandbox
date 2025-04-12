from argparse import _SubParsersAction

from sode.shared.cli import add_subcommand_parsers

from . import thing, track
from .auth.cli import add_auth
from .namespace import SC_COMMAND


def add_command(
    commands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for soundcloud commands"""

    sc_parser = commands.add_parser(
        "soundcloud",
        aliases=["sc"],
        description="Hack SoundCloud",
        help="hack SoundCloud",
    )

    sc_subcommands = add_subcommand_parsers(sc_parser, SC_COMMAND)
    add_auth(sc_subcommands)
    thing.add_subcommand(sc_subcommands)
    track.add_subcommand(sc_subcommands)
