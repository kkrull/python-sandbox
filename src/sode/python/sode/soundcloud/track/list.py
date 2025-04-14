from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from sode.shared.fp.either import Either
from sode.shared.oauth.token import AccessToken

type AccessTokenFactory = Callable[[], Either[str, AccessToken]]


@dataclass(frozen=True)
class ListTracksState:
    access_token: AccessTokenFactory
    user_id: str


# TODO KDK: Work here, then pull data back through the call stack
def list_tracks(state: ListTracksState) -> int:
    # print(f"Listing tracks...", file=state.stdout)
    return 0
