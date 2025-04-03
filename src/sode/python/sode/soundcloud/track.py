import logging
from argparse import _SubParsersAction

from sode.shared.cli import namespace
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.soundcloud.shared import SC_COMMAND


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
    logging.getLogger(__name__).debug(
        {
            "soundcloud-auth": {
                "args": args,
                "command": args.command,
                SC_COMMAND: getattr(args, SC_COMMAND),
                "list": args.list,
            }
        }
    )

    return 0
