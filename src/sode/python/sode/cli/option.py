from argparse import ArgumentParser
from dataclasses import dataclass


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
