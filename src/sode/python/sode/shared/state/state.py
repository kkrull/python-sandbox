import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from sode.shared.fp import Either, Left, Right
from sode.soundcloud.auth.api import TokenResponse


@dataclass(frozen=True)
class SodeState:
    """Top-level saved state for sode"""

    soundcloud_auth: TokenResponse
    version: str

    @staticmethod
    def load(state_file: Path) -> Either[str, "SodeState"]:
        try:
            with open(state_file, mode="rt") as file:
                json_data = json.load(file)
                state = SodeState.parse(json_data)
                return Right(state)
        except Exception as error:
            return Left(str(error))

    @staticmethod
    def parse(data: Mapping[str, Any]) -> "SodeState":
        """Parse from raw data like you get when parsing JSON"""

        return SodeState(
            soundcloud_auth=TokenResponse.parse(data["soundcloud_auth"]),
            version=data["version"],
        )
