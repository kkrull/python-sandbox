#!/usr/bin/env python3

import sys
from argparse import ArgumentError, ArgumentParser, _SubParsersAction
from pprint import pprint
from typing import NoReturn

from sode import version
from sode.cli.state import MainState
from sode.shared.cli import namespace
from sode.shared.cli.namespace import ProgramNamespace, add_command_subparsers, add_global_arguments
from sode.shared.cli.state import RunState

## program module: stuff about the top-level program


def new_main_parser(name: str) -> tuple[  # type: ignore[type-arg]
    ArgumentParser,
    _SubParsersAction,
]:
    main_parser = ArgumentParser(
        add_help=True,
        description="BRODE SODE: Hack away at deadly computing scenarios",
        exit_on_error=False,
        prog=name,
    )

    add_global_arguments(main_parser, version.__version__)
    return (
        main_parser,
        add_command_subparsers(main_parser),
    )


## fs module


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
    namespace.set_parser_command(find_parser, fs_find_run)

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


def fs_find_run(args: ProgramNamespace, state: RunState) -> int:
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


## greet module


def greet_add_parser(
    command_parsers: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    greet_parser = command_parsers.add_parser(
        "greet",
        description="Start with a greeting",
        help="greet somebody",
    )
    namespace.set_parser_command(greet_parser, greet_run)

    greet_parser.add_argument(
        "who",
        default="World",
        help="whom to greet",
        nargs="?",
    )


def greet_run(args: ProgramNamespace, state: RunState) -> int:
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


## sc module: stuff about SoundCloud


def sc_add_parser(
    command_parsers: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    sc_parser = command_parsers.add_parser(
        "soundcloud",
        description="Hack SoundCloud",
        help="hack SoundCloud",
    )
    sc_subcommands = sc_parser.add_subparsers(
        dest="command.soundcloud",
        metavar="SUBCOMMAND",
        title="subcommands",
    )

    sc_auth_add_parser(sc_subcommands)
    sc_track_add_parser(sc_subcommands)


def sc_auth_add_parser(
    sc_subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    sc_auth_parser = sc_subcommands.add_parser(
        "auth",
        description="Authorize with the SoundCloud API",
        help="authorize with SoundCloud API [start here]",
    )
    namespace.set_parser_command(sc_auth_parser, sc_auth_run)

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


def sc_auth_run(args: ProgramNamespace, state: RunState) -> int:
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


def sc_track_add_parser(
    sc_subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    sc_track_parser = sc_subcommands.add_parser(
        "track",
        description="Work with tracks",
        help="hack tracks",
    )
    namespace.set_parser_command(sc_track_parser, sc_track_run)

    sc_track_parser.add_argument(
        "--list",
        action="store_true",
        help="list tracks",
    )


def sc_track_run(args: ProgramNamespace, state: RunState) -> int:
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


## main


def main() -> NoReturn:
    state = MainState(sys.argv)
    status = main_fn(state)
    sys.exit(status)


def main_fn(state: MainState) -> int:
    (main_parser, command_parsers) = new_main_parser(state.program_name)
    fs_add_parser(command_parsers)
    greet_add_parser(command_parsers)
    sc_add_parser(command_parsers)

    try:
        args = main_parser.parse_args(state.arguments, namespace=ProgramNamespace())
    except ArgumentError as error:
        print(str(error), file=state.stderr)
        return 1

    pprint({"main": {"args": args}}, stream=state.stdout)
    return args.run_selected(args, state)


if __name__ == "__main__":
    main()
