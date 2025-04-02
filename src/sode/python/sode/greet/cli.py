from argparse import _SubParsersAction
from pprint import pprint

from sode.shared.cli import namespace
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState


def add_greet(
    command_parsers: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for the greet command"""

    greet_parser = command_parsers.add_parser(
        "greet",
        description="Start with a greeting",
        help="greet somebody",
    )
    namespace.set_parser_command(greet_parser, _greet_run)

    greet_parser.add_argument(
        "who",
        default="World",
        help="whom to greet",
        nargs="?",
    )


def _greet_run(args: ProgramNamespace, state: RunState) -> int:
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
