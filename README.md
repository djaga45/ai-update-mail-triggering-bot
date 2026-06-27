# AI Update Mail Triggering Bot

Automated AI news email agent that sends short, crisp digests at **9:00 AM** and **5:00 PM IST**.

## Features

- Fetches latest AI news from RSS feeds
- Sends professional HTML emails with **Read more** links
- Per-recipient scheduling (morning only / both slots)
- Streamlit dashboard to add recipients
- Windows auto-start support

## Default recipients

| Email | 9 AM IST | 5 PM IST |
|-------|----------|----------|
| jagad*****.com | Yes | Yes |
| jagadeesan*****.com | Yes | Yes |
| bala*****.com | Yes | No |

## Quick start

1. Install Python 3.13+
2. Clone this repo
3. Run `setup_gmail.bat` and enter Gmail App Password
4. Run `start_agent.bat` for the dashboard
5. Run `install_autostart_startup.bat` to start on Windows login

## Manual commands

```bat
py -3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Environment variables

Copy `.env.example` to `.env`:

```
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your-16-char-app-password
FROM_EMAIL=your@gmail.com
```

**Never commit `.env` — it contains secrets.**

