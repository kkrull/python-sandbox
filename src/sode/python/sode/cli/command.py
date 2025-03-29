import io
from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class RunState:
    stderr: io.TextIOBase
    stdout: io.TextIOBase


class CliCommand:
    @abstractmethod
    def run(self, state: RunState) -> int:
        pass
