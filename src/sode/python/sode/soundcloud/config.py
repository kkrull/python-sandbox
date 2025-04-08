import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Response:
    access_token: str
    refresh_token: str


response = Response(access_token="abcdef", refresh_token="ABCDEF")
print(json.dumps(asdict(response), indent=2, sort_keys=True))
