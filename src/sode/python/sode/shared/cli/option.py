import argparse
import re
from typing import Callable


def regex_type(pattern: str | re.Pattern[str]) -> Callable[[str], re.Pattern[str]]:
    """argparse argument type for matching a regex pattern."""

    def closure_check_regex(arg_value: str) -> re.Pattern[str]:
        if not re.match(pattern, arg_value):
            raise argparse.ArgumentTypeError("invalid value")
        return re.compile(arg_value)

    return closure_check_regex
