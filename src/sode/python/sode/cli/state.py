import io
import sys
import typing


class MainState:
    """Everything the program needs to run"""

    _argv: list[str]

    # I/O interfaces that bypass the "any trick" of `TextWrapper | None` typing
    # https://stackoverflow.com/questions/79448057/how-does-maybenone-also-known-as-the-any-trick-work-in-python-type-hints
    stderr: io.TextIOBase
    stdout: io.TextIOBase

    def __init__(
        self,
        argv: list[str],
        stderr: io.TextIOBase = typing.cast(io.TextIOWrapper, sys.stderr),
        stdout: io.TextIOBase = typing.cast(io.TextIOWrapper, sys.stdout),
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
