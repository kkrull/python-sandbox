import typing
from dataclasses import dataclass
from typing import Callable, Iterable, assert_never

from requests import Response

from sode.shared.fp.either import Either, Left, Right
from sode.shared.oauth.token import AccessToken

type AccessTokenFactory = Callable[[], Either[str, AccessToken]]


@dataclass(frozen=True)
class ListTracksState:
    access_token: AccessTokenFactory
    stderr: typing.IO[str]
    stdout: typing.IO[str]
    user_id: str


def list_tracks(state: ListTracksState) -> int:
    match state.access_token().flat_map(
        lambda access_token: _tracks_list(access_token, state.user_id)
    ):
        case Left(err):
            print(err, file=state.stderr)
            return 1
        case Right(listing):
            for name in listing.track_names():
                print(name, file=state.stdout)
            return 0
        case unreachable:
            assert_never(unreachable)


## SoundCloud tracks


@dataclass(frozen=True)
class TrackListing:
    def track_names(self) -> Iterable[str]:
        # TODO KDK: Work here
        return []


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
