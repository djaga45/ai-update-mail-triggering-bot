from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RECIPIENTS_FILE = DATA_DIR / "recipients.json"
SEND_LOG_FILE = DATA_DIR / "send_log.json"
IST = "Asia/Kolkata"
MORNING_HOUR = 9
EVENING_HOUR = 17
AI_NEWS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.artificialintelligence-news.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
]
MAX_HEADLINES = 5
SUMMARY_MAX_CHARS = 140

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = ""
    from_name: str = "AI News Brief"
    dry_run: bool = False

settings = Settings()
DATA_DIR.mkdir(parents=True, exist_ok=True)