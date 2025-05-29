CREATE TABLE IF NOT EXISTS summaries (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	created_at TEXT NOT NULL,
	summary_text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	url TEXT UNIQUE NOT NULL,
	og_title TEXT,
	published_time TEXT,
	og_image TEXT,
	author TEXT,
	text TEXT,
	summary_id INTEGER,
	FOREIGN KEY (summary_id) REFERENCES summaries (id)
);
