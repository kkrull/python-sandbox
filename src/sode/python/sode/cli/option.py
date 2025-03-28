import argparse
import re
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Callable


@dataclass
class BoolOption:
    help: str
    long_name: str
    short_name: str

    def add_to(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            self.short_name,
            self.long_name,
            action="store_true",
            default=False,
            help=self.help,
        )


def regex_type(pattern: str | re.Pattern[str]) -> Callable[[str], re.Pattern[str]]:
    """Argument type for matching a regex pattern."""

    def closure_check_regex(arg_value: str) -> re.Pattern[str]:
        if not re.match(pattern, arg_value):
            raise argparse.ArgumentTypeError("invalid value")
        return re.compile(arg_value)

    return closure_check_regex
