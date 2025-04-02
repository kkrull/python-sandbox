from argparse import _SubParsersAction
from pprint import pprint

from sode.shared.cli import namespace
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState


def add_track(
    sc_subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    sc_track_parser = sc_subcommands.add_parser(
        "track",
        description="Work with tracks",
        help="hack tracks",
    )
    namespace.set_parser_command(sc_track_parser, _run_track)

    sc_track_parser.add_argument(
        "--list",
        action="store_true",
        help="list tracks",
    )


def _run_track(args: ProgramNamespace, state: RunState) -> int:
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
