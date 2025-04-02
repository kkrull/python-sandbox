#!/usr/bin/env python3

import sys
from argparse import ArgumentError, ArgumentParser, Namespace
from pprint import pprint
from typing import NoReturn

from sode import version


def fs_find(args: Namespace) -> int:
    pprint({"fs-find": {"args": args}})
    return 0


def greet(args: Namespace) -> int:
    pprint({"greet": {"args": args}})
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
        dest="command.sode",
        metavar="COMMAND",
        title="commands",
    )
    fs_parser = command_parsers.add_parser(
        "fs",
        description="hack a local filesystem",
        help="hack a local filesystem",
    )
    fs_subcommands = fs_parser.add_subparsers(
        dest="command.fs",
        metavar="SUBCOMMAND",
        title="subcommands",
    )
    find_parser = fs_subcommands.add_parser(
        "find",
        description="find files lurking in the dark",
        help="find files",
    )
    find_parser.set_defaults(func=fs_find)
    find_parser.add_argument(
        "--name",
        help="pattern to match filenames",
        metavar="PATTERN",
        nargs=1,
    )
    find_parser.add_argument(
        "path",
        help="path(s) in which to search for files",
        nargs="+",
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

    pprint({"main": {"args": args}})
    status = args.func(args)
    sys.exit(status)


if __name__ == "__main__":
    main()
