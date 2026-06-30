CREATE TABLE IF NOT EXISTS tags_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER,
    entry_id INTEGER,
    tag TEXT NOT NULL,
    tag_created_at TIMESTAMP NOT NULL,
    tag_deleted_at TIMESTAMP NOT NULl
)



