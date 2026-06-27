import json, smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Literal
from zoneinfo import ZoneInfo
from agent.config import IST, SEND_LOG_FILE, settings
from agent.news_fetcher import NewsItem

Slot = Literal["morning", "evening"]

def _subject(slot, now):
    return f"AI Brief | {'Morning' if slot=='morning' else 'Evening'} Digest — {now.strftime('%d %b %Y')}"

def _html(items, slot, now):
    greeting = "Good morning" if slot=="morning" else "Good evening"
    rows = "".join(f'<tr><td style="padding:14px 0;border-bottom:1px solid #e8edf2;"><p style="margin:0 0 6px;font-size:15px;font-weight:600;color:#0f172a;">{i.title}</p><p style="margin:0 0 8px;font-size:13px;color:#475569;">{i.summary}</p><a href="{i.link}" style="font-size:13px;color:#2563eb;font-weight:600;">Read more →</a></td></tr>' for i in items)
    return f'<html><body style="font-family:Segoe UI,Arial,sans-serif;padding:24px;background:#f8fafc;"><table style="max-width:620px;margin:0 auto;background:#fff;border-radius:12px;"><tr><td style="padding:24px;background:#2563eb;color:#fff;"><h1 style="margin:0;">{greeting} — your AI snapshot</h1><p style="margin:8px 0 0;">{now.strftime("%A, %d %B %Y · %I:%M %p IST")}</p></td></tr><tr><td style="padding:16px 24px;"><table width="100%">{rows}</table></td></tr></table></body></html>'

def _plain(items, slot, now):
    lines = [f"{'Good morning' if slot=='morning' else 'Good evening'} — AI Brief", ""]
    for n,i in enumerate(items,1): lines += [f"{n}. {i.title}", f"   {i.summary}", f"   Read more: {i.link}", ""]
    return "\n".join(lines)

def _sent(slot, recipient, day):
    if not SEND_LOG_FILE.exists(): return False
    with SEND_LOG_FILE.open(encoding="utf-8") as f: log = json.load(f)
    return log.get(day,{}).get(slot,{}).get(recipient, False)

def _mark(slot, recipient, day):
    log = {}
    if SEND_LOG_FILE.exists():
        with SEND_LOG_FILE.open(encoding="utf-8") as f: log = json.load(f)
    log.setdefault(day,{}).setdefault(slot,{})[recipient] = True
    with SEND_LOG_FILE.open("w", encoding="utf-8") as f: json.dump(log, f, indent=2)

def send_digest(recipients, items, slot, force=False):
    if not recipients or not items: return []
    now = datetime.now(ZoneInfo(IST)); day = now.strftime("%Y-%m-%d"); sent = []
    for r in recipients:
        if not force and _sent(slot, r, day): continue
        msg = MIMEMultipart("alternative")
        msg["Subject"] = _subject(slot, now)
        msg["From"] = f"{settings.from_name} <{settings.from_email or settings.smtp_user}>"
        msg["To"] = r
        msg.attach(MIMEText(_plain(items, slot, now), "plain", "utf-8"))
        msg.attach(MIMEText(_html(items, slot, now), "html", "utf-8"))
        if settings.dry_run: print(f"[DRY RUN] Would send to {r}")
        else:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as s:
                s.starttls(); s.login(settings.smtp_user, settings.smtp_password)
                s.sendmail(settings.from_email or settings.smtp_user, [r], msg.as_string())
        _mark(slot, r, day); sent.append(r)
    return sent