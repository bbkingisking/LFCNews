# extractor.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from database import save_article

def extract_frontpage_articles():
    url = "https://www.football365.com/liverpool/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links_set = set()
    main = soup.find("main", class_="w-full lg:w-main")
    if main:
        for a in main.find_all("a", href=True):
            href = a["href"]
            parsed = urlparse(href)
            href = urlunparse(parsed._replace(fragment=""))
            if not href.startswith("https://www.football365.com/news/"):
                continue
            if "/news/author/" in href or "-mediawatch" in href or "-mailbox" in href:
                continue
            links_set.add(href)
    return list(links_set)

def extract_article(conn, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    metadata = {}
    head = soup.find("head")
    if head:
        for tag in head.find_all("meta"):
            if tag.get("property") == "og:title":
                metadata["og:title"] = tag.get("content", "").strip()
            elif tag.get("property") == "article:published_time":
                metadata["article:published_time"] = tag.get("content", "").strip()
            elif tag.get("property") == "og:image":
                metadata["og:image"] = tag.get("content", "").strip()
            elif tag.get("name") == "author":
                metadata["author"] = tag.get("content", "").strip()
    article_section = soup.find("div", class_="ciam-article-f365")
    content_parts = []
    if article_section:
        exclusion_phrases = [
            "READ:", "PREMIER LEAGUE FEATURES ON F365", "Start the conversation",
            "Go Below The Line", "Be the First to Comment",
            "MORE LIVERPOOL COVERAGE ON F365", "READ NOW:", "READ MORE:"
        ]
        for tag in article_section.find_all(["p", "blockquote"]):
            if tag.get("style") == "text-align: center;" or "👉" in tag.get_text():
                continue
            text = tag.get_text(separator=" ", strip=True)
            if any(phrase in text for phrase in exclusion_phrases):
                continue
            content_parts.append(text)
    article_text = "\n\n".join(content_parts)
    save_article(conn, url, metadata, article_text)
    print("Saved", url)
    return {"url": url, "metadata": metadata, "text": article_text}