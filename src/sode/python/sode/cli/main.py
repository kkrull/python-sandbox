#!/usr/bin/env python3

import sys
from argparse import ArgumentError, ArgumentParser
from typing import NoReturn

import sode._version
from sode.cli.state import MainState


def main() -> NoReturn:
    state = MainState(
        argv=sys.argv,
    )

    status = do_main(state)
    sys.exit(status)


def do_main(state: MainState) -> int:
    parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE",
        exit_on_error=False,
        prog=state.program_name(),
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="Log debugging output",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="Print version",
    )

    try:
        args = parser.parse_args(args=state.arguments())
    except ArgumentError as error:
        print(error)
        return 1

    if args.version:
        print(sode._version.__version__)
        return 0

    print("Hello world!")
    return 0


if __name__ == "__main__":
    main()
