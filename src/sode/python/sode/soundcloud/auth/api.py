import json
import logging
from dataclasses import asdict, dataclass
from typing import Any, Mapping, TextIO, Tuple

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from sode.shared.fp import Either, Left, Right
from sode.shared.oauth import AccessToken

from .namespace import ClientId, ClientSecret, TokenUrl

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TokenResponse:
    """How the SoundCloud OAuth2 token endpoint responds"""

    access_token: str
    expires_at: float  # 1743781923.9585016 // datetime.fromtimestamp
    expires_in: int  # 3599 // timedelta(seconds=)
    refresh_token: str
    scope: list[str]  # ['']
    token_type: str  # Bearer

    @property
    def access_token_v(self) -> Either[str, AccessToken]:
        return AccessToken.expected(self.access_token, self.token_type)

    def write_json(
        self,
        writable: TextIO,
        indent: int | str | None = None,
        separators: Tuple[str, str] | None = None,
        sort_keys: bool = False,
    ) -> None:
        """Serialize to JSON and write to the given TextIO"""

        return json.dump(
            asdict(self),
            writable,
            indent=indent,
            separators=separators,
            sort_keys=sort_keys,
        )


def fetch_tokens(
    token_endpoint: TokenUrl, client_id: ClientId, client_secret: ClientSecret
) -> Either[str, TokenResponse]:
    """Request tokens from the specified OAuth2 endpoint using the client_credentials workflow.
    Return either tokens from a successful 2xx response or an error indicating a failed request."""

    logger.debug(
        {
            "fetch_tokens": {
                "client_id": client_id,
                "client_secret": client_secret,
                "token_endpoint": token_endpoint,
            }
        }
    )

    # https://developers.soundcloud.com/docs#authentication
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    try:
        return Right(oauth.fetch_token(auth=auth, token_url=token_endpoint)).map(
            lambda json_response: TokenResponse(**json_response)
        )
    except Exception as err:
        return Left(f"{token_endpoint}: {err}")
