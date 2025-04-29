from requests import Response

from sode.shared.oauth import AccessToken


# TODO KDK: Return Either[str, Playlist] instead of the implementation type Response
def any(access_token: AccessToken, user_id: str) -> Response:
    """Fetch any playlist for a user"""

    # TODO KDK: Switch to user_urn instead of user_id
    # https://developers.soundcloud.com/docs/api/explorer/open-api
    session = access_token.oauth_session()
    return session.get(
        f"https://api.soundcloud.com/users/{user_id}/playlists",
        params={"limit": 1},
    )
