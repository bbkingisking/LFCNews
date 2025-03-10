# database.py

import sqlite3

def get_connection(db_path="lfcarticles.db"):
    return sqlite3.connect(db_path)

def create_table(conn):
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            url TEXT PRIMARY KEY,
            og_title TEXT,
            published_time TEXT,
            og_image TEXT,
            author TEXT,
            text TEXT
        )
    """)
    conn.commit()

def article_exists(conn, url):
    c = conn.cursor()
    c.execute("SELECT 1 FROM articles WHERE url = ?", (url,))
    return c.fetchone() is not None

def save_article(conn, url, metadata, text):
    og_title = metadata.get("og:title", "")
    published_time = metadata.get("article:published_time", "")
    og_image = metadata.get("og:image", "")
    author = metadata.get("author", "")
    c = conn.cursor()
    c.execute("""
        INSERT INTO articles (url, og_title, published_time, og_image, author, text)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (url, og_title, published_time, og_image, author, text))
    conn.commit()