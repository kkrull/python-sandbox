from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ListTracksState:
    state_dir: Path


# TODO KDK: Work here, then pull data back through the call stack
def list_tracks(state: ListTracksState) -> int:
    # print(f"Listing tracks...", file=state.stdout)
    return 0
