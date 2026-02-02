import sqlite3
import os
import logging

from pathlib import Path
from lifelog.storage.base import Storage
from lifelog.core.entry import Entry

logger = logging.getLogger(__name__)

DEBUG_MODE = os.getenv("DEBUG_MODE") == "1"


class DatabaseStorage(Storage):
    def __init__(self, config):
        self.config = config
        if DEBUG_MODE:
            self.db_path = Path(__file__).parent.parent.parent / "dev_diary.db"
        else:
            self.db_path = Path(self.config.paths["diary_db"]).expanduser()
        logger.info(f"Using db {str(self.db_path)}")
        self.schemas_path = Path(__file__).parent / "schemas"
        self.connection = None
        self._setup_database()

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    @property
    def type(self):
        return "database"

    def run_script(self, script):
        if not os.path.exists(script):
            raise FileNotFoundError(f"Unable to find file {script}")

        with open(script, "r") as f:
            sql = f.read()

        try:
            self.connection.executescript(sql)
            self.connection.commit()
            logger.info(f"Executed script {script}")
        except sqlite3.Error as e:
            logger.error(f"Unable to execute script {script}, {e}")

    def _setup_database(self):
        if not os.path.exists(self.db_path):
            logger.info(f"Unable to find database {self.db_path}, creating it.")
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)

        for script in os.listdir(self.schemas_path):
            self.run_script(Path(self.schemas_path / script))

    def add_entry(self, entry):
        query = """
        INSERT INTO entries (timestamp, body)
        VALUES (?, ?)
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (entry.timestamp, entry.body))
            self.connection.commit()

            new_id = cursor.lastrowid

            logger.info(
                f"Inserted entry for timestamp {str(entry.timestamp)} at entry_id {str(new_id)}"
            )

        except sqlite3.Error as e:
            logger.error(f"Failed to insert entry into database: {e}")

    def update_entry(self, old_entry, new_entry):
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO entries_history (entry_id, timestamp, body, archived_at)
                    SELECT entry_id, timestamp, body, ?
                    FROM entries
                    WHERE entry_id = ?;
                """,
                    (str(new_entry.timestamp), old_entry.uid),
                )

                self.connection.execute(
                    """
                    UPDATE entries
                    SET body = ?,
                        updated_at = ?
                    WHERE entry_id = ?;
                """,
                    (new_entry.body, str(new_entry.timestamp), old_entry.uid),
                )

                logger.info(f"Updated entry for uid {str(old_entry.uid)}")

        except sqlite3.Error as e:
            logger.error(f"Failed to update entry for {str(old_entry.uid)}: {e}")

    def open_entry(self, body, timestamp):
        pass

    def get_entries(self) -> list:
        query = """
        SELECT entry_id, timestamp, body
        FROM entries
        ORDER BY entry_id DESC
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()

            entries = []

            for row in cursor:
                logger.info(f"Found row: {row}")

                id = row[0]
                timestamp = row[1]
                body = row[2]

                entry = Entry(
                    timestamp=timestamp,
                    body=body,
                    storage_type="database",
                    uid=id,
                )

                entries.append(entry)

            logger.info(f"Found {len(entries)} entries")
            return entries

        except sqlite3.Error as e:
            logger.error(f"Failed to fetch entries: {e}")
