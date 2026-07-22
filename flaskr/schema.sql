CREATE TABLE IF NOT EXISTS reader (
 reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT,
 bio TEXT,
 offering TEXT,
 location TEXT
 );

CREATE TABLE IF NOT EXISTS sitter (
 sitter_id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT
 );

CREATE TABLE IF NOT EXISTS session (
 session_id INTEGER PRIMARY KEY AUTOINCREMENT,
 reader_id INTEGER,
 sitter_id INTEGER,
 created_at TIMESTAMP DEFAULT (datetime('now','localtime')),
 status TEXT,
 FOREIGN KEY (reader_id) REFERENCES reader(reader_id),
 FOREIGN KEY (sitter_id) REFERENCES sitter(sitter_id)
 );
