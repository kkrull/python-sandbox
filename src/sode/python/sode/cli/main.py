#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import logging
import sys
from argparse import ArgumentError
from typing import NoReturn

import argcomplete

import sode
from sode import version
from sode.cli import parser
from sode.cli.state import MainState
from sode.shared.cli import ProgramNamespace


def main() -> NoReturn:
    state = MainState(sys.argv, version.__version__)
    status = main_fn(state)
    sys.exit(status)


def main_fn(state: MainState) -> int:
    argv_parser = parser.for_argv(state)
    argcomplete.autocomplete(argv_parser, append_space=False)
    try:
        args = argv_parser.parse_args(state.arguments, namespace=ProgramNamespace.empty())
    except ArgumentError as error:
        print(str(error), file=state.stderr)
        return 1

    # Configure logging before accessing logger (getting the order wrong is a world of silent pain).
    args.configure_logging()

    logging.getLogger(sode.__name__).debug({"args": args})
    return args.run_selected(args, state)


if __name__ == "__main__":
    main()
