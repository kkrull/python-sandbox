#!/usr/bin/env python3

import logging
import pprint
import sys
from typing import NoReturn

import sode._version
from sode.cli.args.root import RootArgs, parse_args
from sode.cli.command import CliCommand, RunState
from sode.cli.state import MainState
from sode.shared.either import Left, Right


def main() -> NoReturn:
    state = MainState(argv=sys.argv)
    status = main_fn(state)
    sys.exit(status)


def main_fn(state: MainState) -> int:
    match parse_args(state):
        case Right(args):
            return main_fn_args(state, args)
        case Left(error):
            print(error, file=state.stderr)
            return 1
        case _:
            print(f"Unrecognized argument parse result: {state.arguments}", file=state.stderr)
            return 2


def main_fn_args(state: MainState, args: RootArgs) -> int:
    if args.debug:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

    if args.version:
        print(sode._version.__version__, file=state.stdout)
        return 0

    pprint.pp(args)
    match args.to_command():
        case CliCommand() as command:
            run_state = RunState(stderr=state.stderr, stdout=state.stdout)
            return command.run(run_state)
        case None | _:
            print(f"unknown command: args={args}", file=state.stdout)
            return 2


if __name__ == "__main__":
    main()
