from argparse import ArgumentParser, _SubParsersAction

from sode.shared.cli import namespace
from sode.shared.cli.namespace import CliCommand


def add_unlisted_command(
    commands: _SubParsersAction,  # type: ignore[type-arg]
    name: str,
    description: str,
    command: CliCommand,
) -> ArgumentParser:
    """Make an ArgumentParser which will be omitted from help text, but still runs."""

    parser: ArgumentParser = commands.add_parser(name, description=description)
    namespace.set_parser_command(parser, command)
    return parser
