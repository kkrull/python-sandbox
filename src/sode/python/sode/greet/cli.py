import logging
import os
from argparse import _SubParsersAction

from sode.shared.cli import ProgramNamespace, RunState, argfactory, cmdfactory

logger = logging.getLogger(__name__)


def add_command(
    commands: _SubParsersAction,  # type: ignore[type-arg]
    _environ: os._Environ[str],
) -> None:
    """Add a parser for the greet command"""

    greet_parser = cmdfactory.add_unlisted_command(
        commands,
        "greet",
        command=_greet_run,
        description="Start with a greeting",
    )

    argfactory.completable_argument(
        argfactory.completion_choices(),
        greet_parser.add_argument(
            "who",
            default="World",
            help="whom to greet",
            nargs="?",
        ),
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
