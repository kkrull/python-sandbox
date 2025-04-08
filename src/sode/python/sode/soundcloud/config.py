import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping, TextIO


@dataclass(frozen=True)
class TokenResponse:
    """How the SoundCloud OAuth2 token endpoint responds"""

    access_token: str
    expires_at: float  # 1743781923.9585016
    expires_in: int  # 3599
    refresh_token: str
    scope: list[str]  # ['']
    token_type: str  # Bearer

    @staticmethod
    def from_oauth2_fetch_token(raw_response: Mapping[str, Any]) -> "TokenResponse":
        """Parse from a token response dict that you get from requests_oauthlib"""

        return TokenResponse(**raw_response)

    def to_json(
        self,
        indent: int | str | None = None,
        separators: tuple[str, str] | None = None,
        sort_keys: bool = False,
    ) -> str:
        """Serialize to a JSON str"""

        return json.dumps(
            asdict(self),
            indent=indent,
            separators=separators,
            sort_keys=sort_keys,
        )

    def write_json(
        self,
        fp: TextIO,
        indent: int | str | None = None,
        separators: tuple[str, str] | None = None,
        sort_keys: bool = False,
    ) -> None:
        """Serialize to JSON and write to the given TextIO"""

        return json.dump(
            asdict(self),
            fp,
            indent=indent,
            separators=separators,
            sort_keys=sort_keys,
        )


known_response = TokenResponse(
    access_token="abcdef",
    expires_at=1743781923.9585016,
    expires_in=3599,
    refresh_token="ABCDEF",
    scope=[""],
    token_type="Bearer",
)

fetch_response = TokenResponse.from_oauth2_fetch_token(
    {
        "access_token": "abcdef",
        "expires_at": 1743781923.9585016,
        "expires_in": 3599,
        "refresh_token": "ABCDEF",
        "scope": [""],
        "token_type": "Bearer",
    }
)

print(f"{fetch_response.to_json(indent=2, sort_keys=True)}")
with open("auth-token.json", mode="wt") as file:
    fetch_response.write_json(file, indent=2, sort_keys=True)
