import logging
from argparse import _SubParsersAction

from sode.shared.cli import factory
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState

logger = logging.getLogger(__name__)


def add_greet(
    commands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for the greet command"""

    greet_parser = factory.add_unlisted_command(
        commands,
        "greet",
        command=_greet_run,
        description="Start with a greeting",
    )

    greet_parser.add_argument(
        "who",
        default="World",
        help="whom to greet",
        nargs="?",
    )


def _greet_run(args: ProgramNamespace, state: RunState) -> int:
    logger.debug(
        {
            "greet": {
                "command": args.command,
                "who": args.who,
            }
        }
    )

    print(f"Hello {args.who}", file=state.stdout)
    return 0
