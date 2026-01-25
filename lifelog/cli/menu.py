import logging

from simple_term_menu import TerminalMenu
from lifelog.utils.cli import send_cls
from lifelog.cli.interface import ui, State

logger = logging.getLogger(__name__)


class MenuHandler:
    def __init__(self, app, config):
        self.app = app

        self.menu_options = [
            (
                "n",
                "Create a new entry",
                self.app.entry_handler.create_entry_from_editor,
            ),
            ("r", "Read an entry", self.app.entry_handler.select_and_open_entry),
            (("q", "exit"), "Quit.", self._exit),
        ]

    def _send_header(self):
        send_cls()

        for keys, label, _ in self.menu_options:
            display_key = keys[0] if isinstance(keys, tuple) else keys
            print(f"[{display_key}] {label}")

    def run(self):
        ui.state = State.MENU
        while True:
            self._send_header()

            logging.debug(f"Current buffer: {ui.buffer}")

            choice = input("\nEnter option: ").strip().lower()

            found = False
            for keys, _, func in self.menu_options:
                if choice == keys or (isinstance(keys, tuple) and choice in keys):
                    func()
                    found = True
                    break

            if not found:
                self._send_header()
                input("\nInvalid option. Enter a valid option. ")

    def _exit(self):
        exit(0)


def prompt_selection(items: tuple, title: str, ignore_help: bool = False):
    if not ignore_help:
        title += "\n(Press / and start typing to filter the list)"

    menu_display = [str(item) for item in items]

    terminal_menu = TerminalMenu(
        menu_display,
        title=title,
        menu_cursor="> ",
        menu_cursor_style=("fg_cyan", "bold"),
    )

    selected_index = terminal_menu.show()

    if selected_index is not None:
        return items[selected_index]
