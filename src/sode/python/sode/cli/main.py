#!/usr/bin/env python3

import logging
import logging.config
import sys
from argparse import ArgumentError, ArgumentParser, _SubParsersAction
from typing import NoReturn

from sode import version
from sode.cli.state import MainState
from sode.fs.cli import add_fs
from sode.greet.cli import add_greet
from sode.shared.cli.namespace import ProgramNamespace, add_command_subparsers, add_global_arguments
from sode.soundcloud.cli import add_soundcloud


def main() -> NoReturn:
    state = MainState(sys.argv, version.__version__)
    status = main_fn(state)
    sys.exit(status)


def main_fn(state: MainState) -> int:
    (main_parser, command_parsers) = new_main_parser(state)
    add_fs(command_parsers)
    add_greet(command_parsers)
    add_soundcloud(command_parsers)

    try:
        args = main_parser.parse_args(state.arguments, namespace=ProgramNamespace())
    except ArgumentError as error:
        print(str(error), file=state.stderr)
        return 1

    logging.basicConfig(
        format="""[{name}:{levelname}] {message}""",
        # level=logging.DEBUG,
        style="{",
    )

    logger = logging.getLogger(__name__)
    logger.error("string message")
    logger.error({"message": "object message"})
    logger.debug({"args": args})

    return args.run_selected(args, state)


def new_main_parser(state: MainState) -> tuple[  # type: ignore[type-arg]
    ArgumentParser,
    _SubParsersAction,
]:
    main_parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE: Hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=state.program_name,
    )

    add_global_arguments(main_parser, state.version)
    return (
        main_parser,
        add_command_subparsers(main_parser),
    )


if __name__ == "__main__":
    main()
