import logging
import os
from argparse import _SubParsersAction

import requests

from sode.shared.cli import factory
from sode.shared.cli.namespace import ProgramNamespace
from sode.shared.cli.state import RunState
from sode.soundcloud.shared import SC_COMMAND

logger = logging.getLogger(__name__)


def add_the_thing(
    subcommands: _SubParsersAction,  # type: ignore[type-arg]
) -> None:
    """Add a command that does "the thing" (anything) with SoundCloud"""

    thing_parser = factory.add_unlisted_command(
        subcommands,
        "do-the-thing",
        command=_run_thing,
        description="Do the thing (anything) with SoundCloud, to see if it works",
    )


def _run_thing(args: ProgramNamespace, state: RunState) -> int:
    logger.debug(
        {
            "soundcloud-thing": {
                "client_id": os.environ["SOUNDCLOUD_CLIENT_ID"],
                "client_secret": os.environ["SOUNDCLOUD_CLIENT_SECRET"],
                "command": args.command,
                SC_COMMAND: getattr(args, SC_COMMAND),
            }
        }
    )

    response = requests.get("https://api.soundcloud.com/users/6646206/playlists")
    logger.debug(
        {
            "headers": response.headers,
            "links": response.links,
            "status_code": response.status_code,
        }
    )

    return 0
