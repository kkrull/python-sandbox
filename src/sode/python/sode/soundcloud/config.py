import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Response:
    access_token: str
    expires_in: int
    refresh_token: str

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


response = Response(access_token="abcdef", expires_in=3599, refresh_token="ABCDEF")
print(f"{response.to_json(indent=2, sort_keys=True)}")
