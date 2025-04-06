from argparse import ArgumentParser

from sode.fs.cli import add_fs
from sode.greet.cli import add_greet
from sode.shared.cli import add_command_parsers, add_global_arguments
from sode.soundcloud.cli import add_soundcloud

from .state import MainState


def for_argv(state: MainState) -> ArgumentParser:
    """Create an argument parser-containing sub-parsers for each command-to parse the entire argv"""

    # TODO KDK: Fine-tune argcomplete choices for (sub-)commands
    main_parser = _new_main_parser(state)
    command_parsers = add_command_parsers(main_parser)
    add_fs(command_parsers)
    add_greet(command_parsers)
    add_soundcloud(command_parsers)

    return main_parser


def _new_main_parser(state: MainState) -> ArgumentParser:
    main_parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE: Hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=state.program_name,
    )

    add_global_arguments(main_parser, state.version)
    return main_parser
