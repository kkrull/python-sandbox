#!/usr/bin/env python3

import sys
from argparse import ArgumentError, ArgumentParser
from typing import NoReturn

from sode import version


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

    try:
        args = main_parser.parse_args(sys.argv[1:])
    except ArgumentError as error:
        print(str(error))
        sys.exit(1)

    print(f"args=${args}")
    sys.exit(0)


if __name__ == "__main__":
    main()
