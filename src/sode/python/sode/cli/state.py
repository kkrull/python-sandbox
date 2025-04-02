import sys
import typing

from sode.shared.cli.state import RunState


class MainState(RunState):
    """Everything the program needs to run"""

    _argv: list[str]

    def __init__(
        self,
        argv: list[str],
        stderr: typing.IO[str] = sys.stderr,
        stdout: typing.IO[str] = sys.stdout,
    ):
        super().__init__(stderr=stderr, stdout=stdout)
        self._argv = argv

    @property
    def arguments(self) -> list[str]:
        return self._argv[1:]

    @property
    def program_name(self) -> str:
        return self._argv[0]
