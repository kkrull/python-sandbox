from pathlib import Path


def default_state_dir() -> Path:
    """conventional path where sode persists state between calls"""

    return Path.home().joinpath(".local", "state", "sode")
