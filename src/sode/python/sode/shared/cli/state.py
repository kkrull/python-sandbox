import typing
from logging import Logger


class RunState:
    """Everything a CLI command needs to run"""

    stderr: typing.IO[str]
    stdout: typing.IO[str]

    def __init__(
        self,
        stderr: typing.IO[str],
        stdout: typing.IO[str],
    ):
        self.stderr = stderr
        self.stdout = stdout

    # def logger(self, caller: object) -> Logger:
