import logging
from argparse import _SubParsersAction

import argcomplete

from sode.shared.cli import ProgramNamespace, RunState, argfactory, cmdfactory

logger = logging.getLogger(__name__)


def add_greet(
    commands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for the greet command"""

    greet_parser = cmdfactory.add_unlisted_command(
        commands,
        "greet",
        command=_greet_run,
        description="Start with a greeting",
    )

    argfactory.completable_argument(
        argcomplete.completers.ChoicesCompleter(choices=[]),  # type: ignore[no-untyped-call]
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
