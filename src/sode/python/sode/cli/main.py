#!/usr/bin/env python3

import logging
import sys
from argparse import ArgumentError, ArgumentParser
from typing import NoReturn

import sode._version
from sode.cli.args import SodeNamespace
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
        prog=state.program_name,
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
        args: SodeNamespace = parser.parse_args(args=state.arguments, namespace=SodeNamespace())
    except ArgumentError as error:
        print(error, file=state.stderr)
        return 1

    if args.debug:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
    if args.version:
        print(sode._version.__version__, file=state.stdout)
        return 0

    print("Hello world!", file=state.stdout)
    return 0


if __name__ == "__main__":
    main()
