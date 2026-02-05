import logging
import tempfile
import json

from datetime import datetime
from pathlib import Path

from lifelog.cli.editor import Editor
from lifelog.cli.menu import prompt_selection, prompt_user_input
from lifelog.cli.interface import ui

logger = logging.getLogger(__name__)


class EntryHandler:
    def __init__(self, app, config, storage):
        self.app = app
        self.config = config # TODO use getattr
        self.storage = storage
        # self.entries = entries

    @property
    def entries(self):
        pass

    def create_entry_from_string(self, body):
        entry = Entry(
            timestamp=datetime.now(),
            body=body,
            storage_type=self.storage.type,
        )

        logger.info(
            f"Created entry: {json.dumps({'body': entry.body, 'timestamp': str(entry.timestamp)})}"
        )

        ui.print(f"Created entry: {entry}")

        self.storage.add_entry(entry)

    def create_entry_from_editor(self):
        editor = Editor(self.config.settings["editor"])

        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=self.config.storage["file_extension"], delete=False
        ) as tf:
            temp_path = Path(tf.name)

        try:
            editor.open(temp_path)

            entry = Entry(
                timestamp=datetime.now(),
                body=temp_path.read_text(encoding="utf-8"),
                storage_type=self.storage.type,
            )

            logger.info(
                f"User wrote: {json.dumps({'body': entry.body, 'timestamp': str(entry.timestamp)})}"
            )

            if entry.body != "":
                logger.info("Adding entry...")
                self.storage.add_entry(entry)
                ui.print(f"Created entry: {entry}")

        finally:
            if temp_path.exists():
                temp_path.unlink()

    def edit_entry(self, entry, header=""):
        editor = Editor(self.config.settings["editor"])

        if entry is None:
            logger.warning("Failed to find entry to open in editor")
            return

        new_content = editor.edit_text(entry.body)

        new_entry = Entry(
            timestamp=datetime.now(),
            body=new_content,
            storage_type=self.storage.type,
        )

        if new_entry != entry:
            logger.info(
                f"User updated entry: {json.dumps({'body': new_entry.body, 'timestamp': str(new_entry.timestamp)})}"
            )

            self.storage.update_entry(entry, new_entry)

    def select_entry_cli(self, title="Select an entry: "):
        entries = self.storage.get_entries()

        if len(entries) == 0:
            ui.print("No entries found.")
            logger.warning("No entries found using current storage mode")
            return

        selected_entry = prompt_selection(
            entries,
            title=title,
        )

        if not selected_entry:
            logger.warning("No entry was selected / Unable to find the selected entry")
            return

        logger.info(f"Chose entry: {selected_entry}")
        return selected_entry

    def select_and_open_entry(self):
        selected_entry = self.select_entry_cli(title="\nSelect an entry to view: ")

        if selected_entry:
            self.open_entry_in_editor(selected_entry)

    def select_and_tag_entry(self):
        # TODO fix this function its ugly and too large and should not be here.
        #      most of it should be moved to lifelog/core/tagging.py
        #      also check the other functions in this class if they can be refactored.
        selected_entry = self.select_entry_cli(title="\nSelect an entry to tag: ")

        if not selected_entry:
            logger.warning("No entry was selected / Unable to find the selected entry")
            return

        user_input = prompt_user_input(
            title=f"\nOpen entry in {self.config.settings["editor"]}? [Y/n]: ",
            default="Y",
        )
        if not (user_input == "Y" or user_input == "y"):
            msg = "Editor is the only option for tagging. Rest is NYI!"
            ui.print(f"WARNING: {msg}")
            logger.warning(msg)
            return

        editor = Editor(self.config.settings["editor"])

        body = f"\n# Write the tags you wish to add to this entry on the empty line above separated by a comma: \n# Example: 'fitness, healthy, happy, good day'\n################################################\n{selected_entry.body}"

        content = editor.edit_text(body)
        tags = content.split("\n")[0].split(",")

        if not tags:
            msg = "No tags were provided."
            ui.print(msg)
            return

        ui.print(f"Identified {len(tags)} tags. ({",".join(tags)})")

        if content := ui.flush(): 
            print(f"\n{content}")

        user_input = prompt_user_input(
            title="Apply these tags? [Y/n]:  ",
            default="Y",
        )

        if not (user_input == "Y" or user_input == "y"):
            return

        # TODO fix the DB part.
        #      update schema, make it apply tags if they are missing
        #      might also need some functionality to manage the tags
        #      can maybe be done using edit_entry

class Entry:
    def __init__(self, body, timestamp, storage_type=None, uid=None):
        self.timestamp = timestamp
        self.body = body
        self.storage_type = storage_type
        self.uid = uid

    @property
    def date(self):
        return self.timestamp.date()

    @property
    def time(self):
        return self.timestamp.time()

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = str(value)

    @property
    def storage_type(self):
        return self._storage_type

    @storage_type.setter
    def storage_type(self, value):
        self._storage_type = value.lower()

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    def __str__(self):
        return f"{self.timestamp}"  # Add like 10 words or something from body

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return False

        return self.body == other.body
