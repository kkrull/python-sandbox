#!/usr/bin/env python3

import sys
from argparse import ArgumentParser

import sode._version


def main():
    status = do_main(sys.argv)
    sys.exit(status)


def do_main(argv):
    parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE",
        prog=argv[0],
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="Print version",
    )

    args = parser.parse_args(args=argv[1:])
    if args.version:
        print(f"Version {sode._version.__version__}")
        return 0

    print("Hello world!")
    return 0


if __name__ == "__main__":
    main()
