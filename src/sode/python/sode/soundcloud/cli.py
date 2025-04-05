from argparse import _SubParsersAction

from sode.shared.cli import add_subcommand_parsers

from .auth.cli import add_auth
from .shared import SC_COMMAND
from .thing import add_the_thing
from .track import add_track


def add_soundcloud(
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
    add_the_thing(sc_subcommands)
    add_track(sc_subcommands)
