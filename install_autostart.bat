from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from agent.config import IST, settings
from agent.news_fetcher import fetch_latest_ai_news
from agent.recipients import add_recipient, list_recipients, remove_recipient
from agent.scheduler import run_slot, start_scheduler

st.set_page_config(page_title="AI News Email Agent", layout="wide")
@st.cache_resource
def _scheduler(): return start_scheduler()
_scheduler()
st.title("AI News Email Agent")
st.caption("Automated AI news at **9:00 AM** and **5:00 PM IST**.")
st.info(f"Scheduler running · {datetime.now(ZoneInfo(IST)).strftime('%I:%M %p IST')}")
if st.button("Send test digest now", type="primary"):
    try:
        r = run_slot("morning", force=True)
        st.success(f"Sent {r['sent_count']} email(s) with {r['headline_count']} headlines.")
    except Exception as e: st.error(str(e))
st.subheader("Manage recipients")
with st.form("add"):
    email = st.text_input("Email")
    if st.form_submit_button("Add email", type="primary"):
        ok, msg = add_recipient(email)
        st.success(msg) if ok else st.error(msg)
        if ok: st.rerun()
for r in list_recipients():
    c1,c2 = st.columns([4,1])
    with c1: st.write(f"**{r.email}** — {'9AM+5PM' if r.schedule=='both' else '9AM only'}")
    with c2:
        if not r.builtin and st.button("Remove", key=r.email):
            ok, msg = remove_recipient(r.email)
            if ok: st.rerun()
            else: st.error(msg)