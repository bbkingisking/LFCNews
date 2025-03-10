# Liverpool FC News Summary Bot

An automated tool that scrapes Liverpool FC news articles, generates AI-powered summaries, and delivers them via Telegram and email.

## Overview

This application performs the following tasks:
- Scrapes Liverpool FC news articles from Football365
- Stores article data in a SQLite database
- Uses OpenAI's GPT-4o Mini to generate concise daily summaries
- Delivers summaries through Telegram messages and email notifications
- Maintains a history of previous summaries to avoid repetition

## Features

- **Automated Web Scraping**: Extracts Liverpool FC news articles while filtering out irrelevant content
- **Intelligent Summarization**: Creates fan-focused summaries highlighting transfers, injuries, stats, and match information
- **Multi-channel Delivery**: Distributes summaries via Telegram and email
- **History Tracking**: Avoids repeating information from previous summaries

## Components

- `main.py`: Orchestrates the entire workflow
- `extractor.py`: Handles web scraping of Football365 articles
- `database.py`: Manages SQLite database operations
- `ai_summary.py`: Generates summaries using OpenAI's API
- `send_telegram_message.py`: Handles Telegram message delivery
- `send_email.py`: Handles email delivery

## Requirements

- Python 3.x
- Required packages: in requirements.txt

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   EMAIL_ADDRESS=your_email_address
   EMAIL_PASSWORD=your_email_password
   RECIPIENT_EMAIL_ADDRESS=recipient_email_address
   ```
4. Run the application: `python main.py`

## Usage

The application is designed to run once daily, typically as a scheduled task or cron job. Each run will:
1. Fetch new articles from Football365
2. Generate a fresh summary based on the last 24 hours of news
3. Send the summary via Telegram and email

## Notes

- The summary format includes a one-sentence overview followed by approximately 5 bullet points
- Summaries are written from a Liverpool fan's perspective
- The application uses SMTP via mail.me.com (iCloud) for email delivery
