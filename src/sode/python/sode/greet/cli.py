import logging
from argparse import _SubParsersAction
from pprint import pprint

from sode.shared.cli.factory import add_unlisted_command
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState


def add_greet(
    commands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for the greet command"""

    greet_parser = add_unlisted_command(commands, "greet", "Start with a greeting", _greet_run)
    greet_parser.add_argument(
        "who",
        default="World",
        help="whom to greet",
        nargs="?",
    )


def _greet_run(args: ProgramNamespace, state: RunState) -> int:
    # logging.getLogger(__package__)
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

    print(f"Hello {args.who}", file=state.stdout)
    return 0
