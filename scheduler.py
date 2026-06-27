import html, re
from dataclasses import dataclass
from datetime import datetime, timezone
import feedparser
from agent.config import AI_NEWS_FEEDS, MAX_HEADLINES, SUMMARY_MAX_CHARS

@dataclass
class NewsItem:
    title: str; summary: str; link: str; source: str; published: datetime | None

def _clean(value):
    t = html.unescape(value or "")
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:SUMMARY_MAX_CHARS-3].rstrip()+"..." if len(t) > SUMMARY_MAX_CHARS else t

def fetch_latest_ai_news(limit=MAX_HEADLINES):
    seen, items = set(), []
    for url in AI_NEWS_FEEDS:
        try: parsed = feedparser.parse(url)
        except Exception: continue
        src = parsed.feed.get("title","AI News")
        for e in parsed.entries:
            link = (e.get("link") or "").strip()
            title = _clean(e.get("title",""))
            if not link or not title or link in seen: continue
            summary = _clean(e.get("summary") or e.get("description") or "")
            if not summary: summary = "Latest AI development — tap the link for full context."
            seen.add(link)
            pub = e.get("published_parsed") or e.get("updated_parsed")
            published = datetime(*pub[:6], tzinfo=timezone.utc) if pub else None
            items.append(NewsItem(title, summary, link, src, published))
    items.sort(key=lambda x: x.published or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return items[:limit]