import sqlite3

logger = logging.getLogger(__name__)


class DatabaseHandler:
    def __init__(self, config: config):
        pass

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
