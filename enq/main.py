import logging

from enq.core.entry import EntryHandler
from enq.cli.args import parse_args
from enq.core.logger import setup_logging
from enq.core.config import Config

logger = logging.getLogger(__name__)


def main():
    args = parse_args()

    setup_logging(args.verbose)

    config = Config(args.config_file)

    # TODO add part to override config values with parameters
    # e.g. override storagetype

    entry_handler = EntryHandler(config)

    if args.list_entries:
        entry_handler.list_entries()

    if args.message:
        entry_handler.add_entry(args.message, args.title)

    if args.read_entry:
        entry_handler.read_entry(args.read_entry)

    if args.new:
        entry_handler.get_entry_from_editor()
