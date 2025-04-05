import sys
import typing

from sode.shared.cli import RunState


class MainState(RunState):
    """Everything the program needs to run"""

    _argv: list[str]
    version: str

    def __init__(
        self,
        argv: list[str],
        version: str,
        stderr: typing.IO[str] = sys.stderr,
        stdout: typing.IO[str] = sys.stdout,
    ):
        super().__init__(stderr=stderr, stdout=stdout)
        self._argv = argv
        self.version = version

    @property
    def arguments(self) -> list[str]:
        return self._argv[1:]

    @property
    def program_name(self) -> str:
        return self._argv[0]
