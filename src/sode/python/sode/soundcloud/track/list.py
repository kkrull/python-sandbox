from dataclasses import dataclass
from typing import Callable

from requests import Response

from sode.shared.fp.either import Either, Left
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


## SoundCloud tracks


@dataclass(frozen=True)
class TrackListing:
    pass


def _tracks_list(access_token: AccessToken, user_id: str) -> Either[str, TrackListing]:
    """List all tracks published by a user"""

    return Left("list_tracks: not implemented")


def _tracks_list_raw(access_token: AccessToken, user_id: str) -> Response:
    """List all tracks published by a user, returning the raw HTTP response"""

    # TODO KDK: Look up the actual API endpoint for listing tracks
    session = access_token.oauth_session()
    return session.get(
        f"https://api.soundcloud.com/users/{user_id}/bogus",
        params={"limit": 1},
    )
