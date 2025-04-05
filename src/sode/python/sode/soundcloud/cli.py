from argparse import _SubParsersAction

from sode.shared.cli.namespace import add_subcommand_parsers
from sode.soundcloud.authcmd import add_auth
from sode.soundcloud.shared import SC_COMMAND
from sode.soundcloud.thing import add_the_thing
from sode.soundcloud.track import add_track


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
