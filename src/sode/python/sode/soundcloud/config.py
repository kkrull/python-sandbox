import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    expires_at: float  # 1743781923.9585016
    expires_in: int  # 3599
    refresh_token: str
    scope: list[str]  # ['']
    token_type: str  # Bearer

    @staticmethod
    def from_oauth2_fetch_token(raw_response: Mapping[str, Any]) -> "TokenResponse":
        return TokenResponse(**raw_response)

    def to_json(
        self,
        indent: int | str | None = None,
        separators: tuple[str, str] | None = None,
        sort_keys: bool = False,
    ) -> str:
        return json.dumps(
            asdict(self),
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

api_response = TokenResponse.from_oauth2_fetch_token(
    {
        "access_token": "abcdef",
        "expires_at": 1743781923.9585016,
        "expires_in": 3599,
        "refresh_token": "ABCDEF",
        "scope": [""],
        "token_type": "Bearer",
    }
)


print(f"{api_response.to_json(indent=2, sort_keys=True)}")
