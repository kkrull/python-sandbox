import sys
import typing


class MainState:
    """Everything the program needs to run"""

    _argv: list[str]
    stderr: typing.IO[str]
    stdout: typing.IO[str]

    def __init__(
        self,
        argv: list[str],
        stderr: typing.IO[str] = sys.stderr,
        stdout: typing.IO[str] = sys.stdout,
    ):
        self._argv = argv
        self.stderr = stderr
        self.stdout = stdout

    @property
    def arguments(self) -> list[str]:
        return self._argv[1:]

    @property
    def program_name(self) -> str:
        return self._argv[0]
