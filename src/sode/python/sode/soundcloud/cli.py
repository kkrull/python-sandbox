import os
from argparse import _SubParsersAction

from sode.shared.cli import add_subcommand_parsers

from . import auth, thing, track
from .namespace import SC_COMMAND


def add_command(
    commands: _SubParsersAction,  # type: ignore[type-arg]
    environ: os._Environ[str],
) -> None:
    """Add a parser for soundcloud commands"""

    sc_parser = commands.add_parser(
        "soundcloud",
        aliases=["sc"],
        description="Hack SoundCloud",
        help="hack SoundCloud",
    )

    sc_subcommands = add_subcommand_parsers(sc_parser, SC_COMMAND)
    auth.add_subcommand(sc_subcommands, environ)
    thing.add_subcommand(sc_subcommands, environ)
    track.add_subcommand(sc_subcommands, environ)
