import argparse
import sys

from dataclasses import dataclass

@dataclass(frozen=True)
class CliArgs:

    verbose: bool
    message: str
    list_entries: bool


def parse_args() -> CliArgs:

    parser = argparse.ArgumentParser(
        description="Diary app"
    )

    parser.add_argument(
        "-m", "--message",
        type=str,
        metavar="TEXT",
        help="Write the context of your diary entry as a string."
    )

    parser.add_argument(
        "--list-entries",
        action="store_true",
        help="List entries"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 0.0.1"
    )

    return CliArgs(**vars(parser.parse_args()))

