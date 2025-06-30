CREATE TABLE IF NOT EXISTS context_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    purpose TEXT,
    identity_mode TEXT,
    tension TEXT,
    tags TEXT,
    embedding TEXT
);
