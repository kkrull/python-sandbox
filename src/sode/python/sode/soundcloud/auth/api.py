import logging
from typing import Any, Mapping

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from sode.shared.fp import Either, Left, Right
from sode.shared.oauth import AccessToken

logger = logging.getLogger(__name__)


class TokenResponse:
    """How the SoundCloud OAuth2 token endpoint responds"""

    _mapping: dict[str, Any]
    # access_token: str
    # expires_at: float  # 1743781923.9585016
    # expires_in: int  # 3599
    # refresh_token: str
    # scope: list[str]  # ['']
    # token_type: str  # Bearer

    def __init__(self, raw_response: Mapping[str, Any]):
        self._mapping = dict(raw_response)

    @staticmethod
    def of(raw_response: Mapping[str, Any]) -> "TokenResponse":
        return TokenResponse(raw_response)

    @property
    def access_token(self) -> Either[str, AccessToken]:
        return AccessToken.expected(self._mapping["access_token"], self._mapping["token_type"])


def fetch_tokens(
    token_endpoint: str, client_id: str, client_secret: str
) -> Either[str, TokenResponse]:
    """Authorize with the client_credentials workflow"""

    logger.debug(
        {
            "fetch_tokens": {
                "client_id": repr(client_id),
                "token_url": repr(token_endpoint),
            }
        }
    )

    # https://developers.soundcloud.com/docs#authentication
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    try:
        return Right(oauth.fetch_token(auth=auth, token_url=token_endpoint)).map(
            lambda x: TokenResponse.of(x)
        )
    except Exception as err:
        return Left(f"{token_endpoint}: {err}")
