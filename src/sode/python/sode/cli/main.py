#!/usr/bin/env python3

import sys
from typing import NoReturn

from sode.cli.state import MainState


def main() -> NoReturn:
    state = MainState(argv=sys.argv)
    status = main_fn(state)
    sys.exit(status)


def main_fn(state: MainState) -> int:
    # TODO KDK: Make ArgumentParser in main.  There's really not a good abstraction over a
    # plugin-based architecture where commands add themselves to a namespace that figures out its
    # own command.
    return 0


if __name__ == "__main__":
    main()
