# main.py
import os
from extractor import scrape_latest_articles
from ai_summary import ai_summarize
from send_telegram_message import send_telegram_message
from send_email import send_email

def main():
    scrape_latest_articles()
    summary = ai_summarize()
    send_telegram_message(summary)
    send_email(summary)

if __name__ == '__main__':
    main()
