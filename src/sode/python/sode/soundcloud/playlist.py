from requests import Response

from sode.shared.oauth.token import AccessToken


def any(access_token: AccessToken, user_id: str) -> Response:
    """Fetch any playlist for that user"""

    # https://developers.soundcloud.com/docs/api/explorer/open-api
    session = access_token.oauth_session()
    return session.get(
        f"https://api.soundcloud.com/users/{user_id}/playlists",
        params={"limit": 1},
    )
