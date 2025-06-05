# ai_summary.py
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from openai import OpenAI
from database import get_connection
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_recent_summaries(n=5):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT summary_text
        FROM summaries
        ORDER BY datetime(created_at) DESC
        LIMIT ?
    """, (n,))
    rows = c.fetchall()
    conn.close()
    list_of_summaries = [row[0] for row in rows]
    concatenated_summaries = '\n'.join(list_of_summaries)
    return concatenated_summaries

def fetch_recent_articles():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT url, og_title, text, published_time FROM articles")
    rows = c.fetchall()
    recent_articles = []
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=1)
    for url, title, text, published_time in rows:
        if not published_time:
            continue
        try:
            dt = datetime.fromisoformat(published_time.replace("Z", "+00:00"))
        except Exception:
            continue
        if dt >= cutoff:
            recent_articles.append({
                "Title": title,
                "Text": text,
                "URL": url
            })
    conn.close()
    return recent_articles

def ai_summarize():
    articles = fetch_recent_articles()
    combined_text = "\n\n".join([f"{article['Title']}\n{article['Text']}" for article in articles])
    base_prompt = """
    You are a Liverpool (LFC) fan and supporter. You have access to some news published about the club from the last 24 hours.
    Analyze all the provided articles and create a summary of the key developments and trends from the past 24 hours.
    Begin your message with a ONE-SENTENCE summary stating whether the news is mostly positive, mostly negative, or mixed, and very briefly why.
    Then proceed to more or less 5 short bullet points that summarize the news for the last 24 hours.
    Don't include any other preamble. Separate your bullet points with a newline symbol for better readability.
    Feel free to be biased towards our beloved club. Feel free to use casual language and emojis if appropriate.
    Feel free to ignore articles that are not relevant or that seem to be ads.
    Please do not use clickbait titles, summaries, or language. Be concise. Do not include live streaming information.
    The most important areas that fans would care about are completed/potential transfers, injuries, player/team stats, and match summaries/previews.
    """
    recent_summaries = load_recent_summaries()
    if recent_summaries:
        history_instruction = f"Below are the 5 previous summaries you generated: {recent_summaries} Do not repeat the exact same points and phrasings from your previous summaries. Progress on the previous stories is obviously allowed."
        system_prompt = f"{base_prompt} \n {history_instruction}"
    else:
        system_prompt = base_prompt

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": f"{system_prompt}\n\n{combined_text}"}],
            temperature=0.7,
            max_tokens=1000
        )
        summary_text = response.choices[0].message.content
        save_summary(summary_text, articles)
        return summary_text
    except Exception as e:
        print(f"Error connecting to OpenAI API: {e}")
        raise

def save_summary(summary_text, articles):
    conn = get_connection()
    c = conn.cursor()

    # Save new summary
    created_at = datetime.now(timezone.utc).isoformat()
    c.execute("""
        INSERT INTO summaries (created_at, summary_text)
        VALUES (?, ?)
    """, (created_at, summary_text))
    summary_id = c.lastrowid

    # Update articles with new summary_id
    for article in articles:
        c.execute("""
            UPDATE articles
            SET summary_id = ?
            WHERE url = ?
        """, (summary_id, article["URL"]))

    conn.commit()
    conn.close()
