# main.py

import os
from database import get_connection, create_table, article_exists
from extractor import extract_frontpage_articles, extract_article
from ai_summary import ai_summarize
from send_telegram_message import send_telegram_message
from send_email import send_email
from datetime import datetime

def save_summary(summary):
    now = os.path.dirname(os.path.abspath(__file__))
    history_dir = os.path.join(now, "history")
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    filename = datetime.now().strftime("%y%m%d") + ".txt"
    with open(os.path.join(history_dir, filename), "w", encoding="utf-8") as f:
        f.write(summary)

def main():
    conn = get_connection()
    create_table(conn)
    urls = extract_frontpage_articles()
    for url in urls:
        if not article_exists(conn, url):
            extract_article(conn, url)
    conn.close()
    summary = ai_summarize()
    send_telegram_message(summary)
    send_email(summary)
    save_summary(summary)
if __name__ == '__main__':
    main()