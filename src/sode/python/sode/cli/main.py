#!/usr/bin/env python3

import logging
import sys
import typing
from typing import NoReturn

import sode._version
from sode.cli.args import SodeNamespace, parse_args
from sode.cli.state import MainState


def main() -> NoReturn:
    state = MainState(
        argv=sys.argv,
    )

    status = do_main(state)
    sys.exit(status)


def do_main(state: MainState) -> int:
    args: str | SodeNamespace = parse_args(state)
    if args is str:
        print(args, file=state.stderr)
        return 1

    # Try making typings for Either: https://stackoverflow.com/a/62282621/112682
    sodeArgs = typing.cast(SodeNamespace, args)
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
