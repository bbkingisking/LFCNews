# database.py
import sqlite3
import os

def get_connection(db_path="lfcarticles.db"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "lfcarticles.db")
    return sqlite3.connect(db_path)

def create_table(conn):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
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
