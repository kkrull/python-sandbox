from argparse import _SubParsersAction
from pprint import pprint

from sode.shared.cli import namespace
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState


def add_greet(
    commands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a parser for the greet command"""

    # Provide the command, but don't list it in the help
    greet_parser = commands.add_parser(
        "greet",
        description="Start with a greeting",
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

    print(f"Hello {args.who}", file=state.stdout)
    return 0
