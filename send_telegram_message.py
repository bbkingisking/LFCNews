# send_telegram_message.py

import os
import telebot
from dotenv import load_dotenv
load_dotenv()

def clean_markdown(text):
    chars_to_escape = ['_', '[', ']', '(', ')', '~', '`', '>', '#', '+', '=', '|', '{', '}', '.', '!']
    result = text
    result = result.replace("\n- ", "\n\\- ")
    result = result.replace("\n* ", "\n\\* ")
    result = result.replace("-", "\\-").replace("\n\\\\- ", "\n\\- ")
    for char in chars_to_escape:
        result = result.replace(char, '\\' + char)
    return result

def send_telegram_message(message):
    bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
    try:
        cleaned_message = clean_markdown(message)
        if len(cleaned_message) > 4000:
            chunks = [cleaned_message[i:i+4000] for i in range(0, len(cleaned_message), 4000)]
            for chunk in chunks:
                bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), chunk, parse_mode='MarkdownV2')
        else:
            bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), cleaned_message, parse_mode='MarkdownV2')
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        try:
            plain_message = message.replace('*', '')
            if len(plain_message) > 4000:
                chunks = [plain_message[i:i+4000] for i in range(0, len(plain_message), 4000)]
                for chunk in chunks:
                    bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), chunk)
            else:
                bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), plain_message)
        except Exception as e2:
            print(f"Error sending fallback plain message: {e2}")
            raise