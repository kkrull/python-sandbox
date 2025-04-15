import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, TextIO

from sode.shared.fp import Either, Left
from sode.soundcloud.auth.api import TokenResponse


@dataclass(frozen=True)
class SodeState:
    """Top-level saved state for sode"""

    soundcloud_auth: TokenResponse

    @staticmethod
    def load(state_file: Path) -> Either[str, "SodeState"]:
        try:
            with open(state_file, mode="rt") as file:
                json_file = json.load(file)
            return Left("SodeState::load: not implemented")
        except Exception as error:
            return Left(str(error))

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
