from argparse import ArgumentParser, HelpFormatter, _SubParsersAction
from typing import Any

from sode.shared.cli import namespace
from sode.shared.cli.namespace import CliCommand


def add_command(
    commands: _SubParsersAction,  # type: ignore[type-arg]
    name: str,
    command: CliCommand,
    description: str = "",
    epilog: str = "",
    formatter_class: Any = HelpFormatter,
    help: str = "",
) -> ArgumentParser:
    """Make an ArgumentParser which will be omitted from help text, but still runs."""

    parser: ArgumentParser = commands.add_parser(
        name,
        description=description,
        epilog=epilog,
        formatter_class=formatter_class,
        help=help,
    )

    namespace.set_parser_command(parser, command)
    return parser


def add_unlisted_command(
    commands: _SubParsersAction,  # type: ignore[type-arg]
    name: str,
    command: CliCommand,
    description: str = "",
) -> ArgumentParser:
    """Make an ArgumentParser which will be omitted from help text, but still runs."""

    parser: ArgumentParser = commands.add_parser(name, description=description)
    namespace.set_parser_command(parser, command)
    return parser
