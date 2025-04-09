import json
import typing
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
    def parse(data: Mapping[str, Any]) -> "TokenResponse":
        """Parse data from JSON data like you get when fetching tokens with requests_oauthlib"""

        return TokenResponse(**data)

    @staticmethod
    def read_json(readable: TextIO) -> "TokenResponse":
        """Read from a given TextIO and parse as JSON"""

        return TokenResponse.parse(json.load(readable))

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
        writable: TextIO,
        indent: int | str | None = None,
        separators: tuple[str, str] | None = None,
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


@dataclass(frozen=True)
class SodeState:
    """Top-level saved state for sode"""

    soundcloud_auth: TokenResponse

    @staticmethod
    def parse(data: Mapping[str, Any]) -> "SodeState":
        """Parse from raw data like you get when parsing JSON"""

        return SodeState(**data)

    @staticmethod
    def read_json(readable: TextIO) -> "SodeState":
        """Read from a given TextIO and parse as JSON"""

        return SodeState.parse(json.load(readable))

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


known_response = TokenResponse(
    access_token="abcdef",
    expires_at=1743781923.9585016,
    expires_in=3599,
    refresh_token="ABCDEF",
    scope=[""],
    token_type="Bearer",
)

fetch_response = TokenResponse.parse(
    {
        "access_token": "abcdef",
        "expires_at": 1743781923.9585016,
        "expires_in": 3599,
        "refresh_token": "ABCDEF",
        "scope": [""],
        "token_type": "Bearer",
    }
)


print(f"fetch_response={fetch_response.to_json(indent=2, sort_keys=True)}")
with open("auth-token.json", mode="wt") as file:
    fetch_response.write_json(file, indent=2, sort_keys=True)

with open("auth-token.json", mode="rt") as file:
    file_response = TokenResponse.read_json(file)
    print(f"file_response={file_response.to_json(indent=2, sort_keys=True)}")

with open("sode-state.json", mode="rt") as file:
    state_raw = json.load(file)
    print(f"state_raw={json.dumps(state_raw, indent=2, sort_keys=True)}")

with open("sode-state.json", mode="rt") as file:
    state = SodeState.read_json(file)
    print(f"state={state.to_json(indent=2, sort_keys=True)}")
    print(f"state={state!r}")
