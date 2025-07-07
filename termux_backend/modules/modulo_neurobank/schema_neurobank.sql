CREATE TABLE IF NOT EXISTS neuro_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    action TEXT NOT NULL,
    amount INTEGER NOT NULL,
    input_id INTEGER,
    metadata TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS neuro_nfts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_id INTEGER NOT NULL,
    title TEXT,
    metadata TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    module TEXT NOT NULL
);
