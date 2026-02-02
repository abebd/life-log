import argparse
import os

from dataclasses import dataclass
from importlib.metadata import version as get_version


@dataclass(frozen=True)
class CliArgs:
    verbose: bool
    message: str
    read_entries: bool
    new: bool
    config_file: str


def parse_args() -> CliArgs:
    parser = argparse.ArgumentParser(description="Diary app")

    parser.add_argument(
        "-n", "--new", action="store_true", help="open an editor and write an entry"
    )

    parser.add_argument(
        "-r",
        "--read-entries",
        action="store_true",
        help="select entries from a list and read or edit it",
    )

    parser.add_argument(
        "-m", "--message", type=str, metavar="TEXT", help="write a quick diary entry"
    )

    __version__ = get_version("lifelog")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    DEBUG_MODE = os.getenv("DEBUG_MODE") == "1"
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="enable verbose output. can also be enabled by setting DEBUG=1",
        default=DEBUG_MODE,
    )

    parser.add_argument(
        "--config-file", type=str, metavar="TEXT", help="specify the config file to use"
    )

    # Print out args if none were provided
    # NOTE: no longer used since we have the MenuHandler
    # args = parser.parse_args()
    #
    # if len(sys.argv) == 1:
    #    parser.print_help()
    #    sys.exit(1)

    return CliArgs(**vars(parser.parse_args()))
