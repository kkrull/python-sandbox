import logging
from argparse import _SubParsersAction

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
    logger = logging.getLogger(_greet_run.__module__)
    logger.debug(
        {
            "greet": {
                "args": args,
                "command": args.command,
                "who": args.who,
            }
        }
    )

    print(f"Hello {args.who}", file=state.stdout)
    return 0
