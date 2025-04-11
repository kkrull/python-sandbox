import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Mapping, TextIO


@dataclass(frozen=True)
class TokenResponse2:
    """How the SoundCloud OAuth2 token endpoint responds"""

    access_token: str
    expires_at: float  # 1743781923.9585016 // datetime.fromtimestamp
    expires_in: int  # 3599 // timedelta(seconds=)
    refresh_token: str
    scope: list[str]  # ['']
    token_type: str  # Bearer

    @staticmethod
    def parse(data: Mapping[str, Any]) -> "TokenResponse2":
        """Parse data from JSON data like you get when fetching tokens with requests_oauthlib"""

        return TokenResponse2(**data)

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


@dataclass(frozen=True)
class SodeState1:
    """Top-level saved state for sode"""

    soundcloud_auth: TokenResponse2

    @staticmethod
    def parse(data: Mapping[str, Any]) -> "SodeState1":
        """Parse from raw data like you get when parsing JSON"""

        return SodeState1(
            soundcloud_auth=TokenResponse2.parse(data["soundcloud_auth"]),
        )

    @staticmethod
    def read_json(readable: TextIO) -> "SodeState1":
        """Read from a given TextIO and parse as JSON"""

        return SodeState1.parse(json.load(readable))
