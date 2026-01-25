import logging

from importlib.metadata import version as get_version

from lifelog.core.entry import EntryHandler
from lifelog.cli.args import parse_args
from lifelog.core.logger import setup_logging
from lifelog.core.config import Config
from lifelog.cli.menu import MenuHandler
from lifelog.cli.interface import ui
from lifelog.storage.database import DatabaseStorage
from lifelog.storage.file import FileStorage

logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        self.args = parse_args()

        setup_logging(self.args.verbose)

        logger.debug(f"-----| Starting run @ lifelog-{get_version('lifelog')} |-----")
        logger.debug(f"Current state: {ui.state}")
        logger.debug(f"Args passed from user: {self.args}")

        self.config = Config(self.args.config_file)

        if self.config.settings["storage_mode"] == "database":
            logger.debug("Using storage type database")
            self.storage = DatabaseStorage(self.config)
        else:
            logger.debug("Using storage type file")
            self.storage = FileStorage(self.config)

        self.entry_handler = EntryHandler(self.config, self.storage)
        self.menu_handler = MenuHandler(self, self.config)

    def run(self):
        ran_something = False

        if self.args.read_entries:
            ran_something = True
            self.entry_handler.select_and_open_entry()

        if self.args.message:
            ran_something = True
            self.entry_handler.create_entry_from_string(self.args.message)

        if self.args.new:
            ran_something = True
            self.entry_handler.create_entry_from_editor()

        # If nothing ran, open the interactive menu
        if not ran_something:
            self.menu_handler.run()


def main():
    app = App()
    app.run()
