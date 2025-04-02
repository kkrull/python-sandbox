from argparse import _SubParsersAction
from pprint import pprint

from sode.shared.cli import namespace
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.soundcloud.cli import SC_COMMAND


def add_track(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add the track sub-command"""
    track_parser = subcommands.add_parser(
        "track",
        description="Work with tracks",
        help="hack tracks",
    )
    namespace.set_parser_command(track_parser, _run_track)

    track_parser.add_argument(
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
                SC_COMMAND: getattr(args, SC_COMMAND),
                "debug": args.debug,
                "list": args.list,
            }
        },
        stream=state.stdout,
    )

    return 0
