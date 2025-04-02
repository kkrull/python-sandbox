#!/usr/bin/env python3

import sys
from argparse import ArgumentError, ArgumentParser, Namespace
from pprint import pprint
from typing import Callable, NoReturn

from sode import version


class SodeNamespace(Namespace):
    run_selected: Callable[["SodeNamespace"], int]


def fs_find(args: Namespace) -> int:
    pprint(
        {
            "fs-find": {
                "args": args,
                "command": args.command,
                "command.fs": getattr(args, "command.fs"),
                "name": args.name,
                "path": args.path,
            }
        }
    )
    return 0


def greet(args: Namespace) -> int:
    pprint(
        {
            "greet": {
                "args": args,
                "command": args.command,
                "who": args.who,
            }
        }
    )
    return 0


def sc_auth(args: Namespace) -> int:
    pprint(
        {
            "soundcloud-auth": {
                "args": args,
                "command": args.command,
                "command.soundcloud": getattr(args, "command.soundcloud"),
                "check_token_expiration": args.check_token_expiration,
                "client_id": args.client_id,
                "client_secret": args.client_secret,
            }
        }
    )
    return 0


def sc_track(args: Namespace) -> int:
    pprint(
        {
            "soundcloud-auth": {
                "args": args,
                "command": args.command,
                "command.soundcloud": getattr(args, "command.soundcloud"),
                "list": args.list,
            }
        }
    )
    return 0


def main() -> NoReturn:
    main_parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE: Hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=sys.argv[0],
    )

    main_parser.add_argument(
        "--version",
        action="version",
        version=version.__version__,
    )

    command_parsers = main_parser.add_subparsers(
        dest="command",
        metavar="COMMAND",
        title="commands",
    )
    fs_parser = command_parsers.add_parser(
        "fs",
        description="Hack a local filesystem",
        help="hack a local filesystem",
    )
    fs_subcommands = fs_parser.add_subparsers(
        dest="command.fs",
        metavar="SUBCOMMAND",
        title="subcommands",
    )
    find_parser = fs_subcommands.add_parser(
        "find",
        description="Find files lurking in the dark",
        help="find files",
    )
    find_parser.set_defaults(run_selected=fs_find)
    find_parser.add_argument(
        "--name",
        help="pattern to match filenames",
        metavar="PATTERN",
        nargs=1,
    )
    find_parser.add_argument(
        "path",
        help="path(s) in which to search for files",
        nargs="+",
    )

    greet_parser = command_parsers.add_parser(
        "greet",
        description="Start with a greeting",
        help="greet somebody",
    )
    greet_parser.set_defaults(run_selected=greet)
    greet_parser.add_argument(
        "who",
        default="World",
        help="whom to greet",
        nargs="?",
    )

    soundcloud_parser = command_parsers.add_parser(
        "soundcloud",
        description="Hack SoundCloud",
        help="hack SoundCloud",
    )
    soundcloud_subcommands = soundcloud_parser.add_subparsers(
        dest="command.soundcloud",
        metavar="SUBCOMMAND",
        title="subcommands",
    )
    sc_auth_parser = soundcloud_subcommands.add_parser(
        "auth",
        description="Authorize with the SoundCloud API",
        help="authorize with SoundCloud API [start here]",
    )
    sc_auth_parser.set_defaults(run_selected=sc_auth)
    sc_auth_parser.add_argument(
        "--check-token-expiration",
        action="store_true",
        help="check if persisted access token has expired",
    )
    sc_auth_parser.add_argument(
        "--client-id",
        help="OAuth2 client id with which to request access",
        nargs="?",
    )
    sc_auth_parser.add_argument(
        "--client-secret",
        help="OAuth2 client secret with which to request access",
        nargs="?",
    )

    sc_track_parser = soundcloud_subcommands.add_parser(
        "track",
        description="Work with tracks",
        help="hack tracks",
    )
    sc_track_parser.set_defaults(run_selected=sc_track)
    sc_track_parser.add_argument(
        "--list",
        action="store_true",
        help="list tracks",
    )

    try:
        args = main_parser.parse_args(sys.argv[1:], namespace=SodeNamespace())
    except ArgumentError as error:
        print(str(error))
        sys.exit(1)

    pprint({"main": {"args": args}})
    status = args.run_selected(args)
    sys.exit(status)


if __name__ == "__main__":
    main()
