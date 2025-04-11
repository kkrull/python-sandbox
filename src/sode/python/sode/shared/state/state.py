import json
from dataclasses import dataclass
from typing import Any, Mapping, TextIO

from sode.soundcloud.auth.api import TokenResponse


@dataclass(frozen=True)
class SodeState:
    """Top-level saved state for sode"""

    soundcloud_auth: TokenResponse

    @staticmethod
    def parse(data: Mapping[str, Any]) -> "SodeState":
        """Parse from raw data like you get when parsing JSON"""

        return SodeState(
            soundcloud_auth=TokenResponse.parse(data["soundcloud_auth"]),
        )

    @staticmethod
    def read_json(readable: TextIO) -> "SodeState":
        """Read from a given TextIO and parse as JSON"""

        return SodeState.parse(json.load(readable))
