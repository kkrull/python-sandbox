import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
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

    @staticmethod
    def parse(data: Mapping[str, Any]) -> "TokenResponse":
        """Parse data from JSON data like you get when fetching tokens with requests_oauthlib"""

        return TokenResponse(**data)

    @property
    def access_token_v(self) -> Either[str, AccessToken]:
        return AccessToken.expected(self.access_token, self.token_type)

    @property
    def expiration(self) -> datetime:
        """the datetime at which this access token expires"""

        return datetime.fromtimestamp(self.expires_at)

    @property
    def expired(self, now: datetime = datetime.now()) -> bool:
        """true if the access token has expired; false if not"""

        return self.expiration > now

    @property
    def remaining_time(self, now: datetime = datetime.now()) -> timedelta:
        """how much time is left before the access token expires, or 0 if it has already expired"""

        if self.expiration <= now:
            return timedelta()
        else:
            return self.expiration - now

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
                "token_endpoint": token_endpoint,
            }
        }
    )

    # https://developers.soundcloud.com/docs#authentication
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    try:
        response: Mapping[str, Any] = oauth.fetch_token(auth=auth, token_url=token_endpoint)
        return Right(response).map(lambda json: TokenResponse(**json))
    except Exception as err:
        return Left(f"{token_endpoint}: {err}")
