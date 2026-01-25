CREATE TABLE IF NOT EXISTS entries_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    body TEXT NOT NULL,
    archived_at TIMESTAMP NOT NULL
)
