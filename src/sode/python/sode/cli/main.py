#!/usr/bin/env python3

import sys
from argparse import ArgumentError, ArgumentParser, Namespace, _SubParsersAction
from pprint import pprint
from typing import Callable, NoReturn

from sode import version
from sode.cli.state import MainState


class CommandNamespace(Namespace):
    command: str
    debug: bool
    run_selected: Callable[["CommandNamespace", MainState], int]


def fs_add_parser(
    command_parsers: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
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

    fs_find_add_parser(fs_subcommands)


def fs_find_add_parser(
    fs_subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    find_parser = fs_subcommands.add_parser(
        "find",
        description="Find files lurking in the dark",
        help="find files",
    )
    find_parser.set_defaults(run_selected=fs_find_run)
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


def fs_find_run(args: CommandNamespace, state: MainState) -> int:
    pprint(
        {
            "fs-find": {
                "args": args,
                "command": args.command,
                "command.fs": getattr(args, "command.fs"),
                "debug": args.debug,
                "name": args.name,
                "path": args.path,
            }
        },
        stream=state.stdout,
    )

    return 0


def greet_add_parser(
    command_parsers: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    greet_parser = command_parsers.add_parser(
        "greet",
        description="Start with a greeting",
        help="greet somebody",
    )
    greet_parser.set_defaults(run_selected=greet_run)
    greet_parser.add_argument(
        "who",
        default="World",
        help="whom to greet",
        nargs="?",
    )


def greet_run(args: CommandNamespace, state: MainState) -> int:
    pprint(
        {
            "greet": {
                "args": args,
                "command": args.command,
                "debug": args.debug,
                "who": args.who,
            }
        },
        stream=state.stdout,
    )

    return 0


def sc_auth(args: CommandNamespace, state: MainState) -> int:
    pprint(
        {
            "soundcloud-auth": {
                "args": args,
                "command": args.command,
                "command.soundcloud": getattr(args, "command.soundcloud"),
                "check_token_expiration": args.check_token_expiration,
                "client_id": args.client_id,
                "client_secret": args.client_secret,
                "debug": args.debug,
            }
        },
        stream=state.stdout,
    )

    return 0


def sc_track(args: CommandNamespace, state: MainState) -> int:
    pprint(
        {
            "soundcloud-auth": {
                "args": args,
                "command": args.command,
                "command.soundcloud": getattr(args, "command.soundcloud"),
                "debug": args.debug,
                "list": args.list,
            }
        },
        stream=state.stdout,
    )

    return 0


def main() -> NoReturn:
    state = MainState(sys.argv)
    status = main_fn(state)
    sys.exit(status)


def main_fn(state: MainState) -> int:
    main_parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE: Hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=state.program_name,
    )

    main_parser.add_argument(
        "--debug",
        action="store_true",
        help="turn on the debug logger",
    )
    main_parser.add_argument(
        "--version",
        action="version",
        version=version.__version__,
    )

    command_parsers = main_parser.add_subparsers(
        dest="command",
        metavar="COMMAND",
        required=True,
        title="commands",
    )

    fs_add_parser(command_parsers)
    greet_add_parser(command_parsers)

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
        args = main_parser.parse_args(state.arguments, namespace=CommandNamespace())
    except ArgumentError as error:
        print(str(error), file=state.stderr)
        return 1

    pprint({"main": {"args": args}}, stream=state.stdout)
    return args.run_selected(args, state)


if __name__ == "__main__":
    main()
