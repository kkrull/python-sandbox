#!/usr/bin/env python3

import sys
from argparse import ArgumentError, ArgumentParser, Namespace
from typing import NoReturn

from sode import version


def greet(args: Namespace) -> int:
    print(f"[greet] args=${args}")
    return 0


def main() -> NoReturn:
    main_parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE: hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=sys.argv[0],
    )

    main_parser.add_argument(
        "--version",
        action="version",
        version=version.__version__,
    )

    command_parsers = main_parser.add_subparsers(
        dest="command",
        metavar="COMMAND",
        title="commands",
    )
    greet_parser = command_parsers.add_parser(
        "greet",
        description="start with a greeting",
        help="greet somebody",
    )
    greet_parser.add_argument(
        "who",
        default="World",
        help="whom to greet",
        nargs="?",
    )
    greet_parser.set_defaults(func=greet)

    try:
        args = main_parser.parse_args(sys.argv[1:])
    except ArgumentError as error:
        print(str(error))
        sys.exit(1)

    print(f"args=${args}")
    status = args.func(args)
    sys.exit(status)


if __name__ == "__main__":
    main()
