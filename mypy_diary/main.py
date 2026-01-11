import logging

from mypy_diary.core.handler import MessageHandler, EntryHandler
from mypy_diary.cli.arg_parser import CliArgs, parse_args
from mypy_diary.core.logger import setup_logging
from mypy_diary.core.config import Config

logger = logging.getLogger(__name__)

def main():

    args = parse_args()
    setup_logging(args.verbose)

    config = Config()

    if args.list_entries:
        entry_handler = EntryHandler(config)
        entry_handler.list_entries()

    if args.message:
        message_handler = MessageHandler(config)
        message_handler(content=args.message)
        

