import typing
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, assert_never

import requests
from requests import Response
from requests_oauthlib import OAuth2Session

from sode.shared.fp import Either, Left, Right
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
    @staticmethod
    def parse(response_data: Mapping[str, Any]) -> Either[str, "TrackListing"]:
        return Left("TrackListing::parse: not implemented")

    def track_names(self) -> Iterable[str]:
        # TODO KDK: Work here
        return []


def _tracks_list(access_token: AccessToken, user_id: str) -> Either[str, TrackListing]:
    """List all tracks published by a user"""

    return (
        Right[str, OAuth2Session](access_token.oauth_session())
        .map(lambda session: _tracks_list_raw(session, user_id))
        .flat_map(lambda response: _response_to_either(response))
        .map(lambda http_response: http_response.json())
        .flat_map(lambda json_response: TrackListing.parse(json_response))
    )


def _tracks_list_raw(session: requests.Session, user_id: str) -> Response:
    """List all tracks published by a user, returning the raw HTTP response"""

    # TODO KDK: Look up the actual API endpoint for listing tracks
    return session.get(
        f"https://api.soundcloud.com/me/tracks",
        params={"limit": 1},
    )


def _response_to_either(response: Response) -> Either[str, Response]:
    if response.ok:
        return Right(response)
    else:
        return Left(
            f"Response indicates failure: status={response.status_code}, text={response.text}"
        )
