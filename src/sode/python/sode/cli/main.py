#!/usr/bin/env python3

import logging
import sys
from typing import NoReturn

import sode._version
from sode.cli.args import SodeNamespace, parse_args
from sode.cli.state import MainState
from sode.shared.either import Either, Left, Right


def main() -> NoReturn:
    state = MainState(argv=sys.argv)
    status = mainFn(state)
    sys.exit(status)


def mainFn(state: MainState) -> int:
    args: Either[str, SodeNamespace] = parse_args(state)
    match args:
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case Right(sodeArgs):
            return mainFnArgs(state, sodeArgs)
        case _:
            print(f"Unrecognized argument parse result: {args}", file=state.stderr)
            return 2


def mainFnArgs(state: MainState, sodeArgs: SodeNamespace) -> int:
    if sodeArgs.debug:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

    if sodeArgs.version:
        print(sode._version.__version__, file=state.stdout)
        return 0

    print("Hello world!", file=state.stdout)
    return 0


if __name__ == "__main__":
    main()
