import json, re
from dataclasses import dataclass
from typing import Literal
from agent.config import RECIPIENTS_FILE

Schedule = Literal["both", "morning_only", "evening_only"]
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

@dataclass
class Recipient:
    email: str
    schedule: Schedule
    builtin: bool = False

def _load_raw():
    if not RECIPIENTS_FILE.exists(): return {"recipients": []}
    with RECIPIENTS_FILE.open(encoding="utf-8") as f: return json.load(f)

def _save_raw(data):
    RECIPIENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RECIPIENTS_FILE.open("w", encoding="utf-8") as f: json.dump(data, f, indent=2)

def list_recipients():
    return [Recipient(email=i["email"].strip().lower(), schedule=i.get("schedule","both"), builtin=bool(i.get("builtin",False))) for i in _load_raw().get("recipients",[])]

def add_recipient(email, schedule="both"):
    n = email.strip().lower()
    if not EMAIL_PATTERN.match(n): return False, "Enter a valid email address."
    rs = list_recipients()
    if any(r.email == n for r in rs): return False, "This email is already on the list."
    rs.append(Recipient(email=n, schedule=schedule, builtin=False))
    _save_raw({"recipients": [{"email": r.email, "schedule": r.schedule, "builtin": r.builtin} for r in rs]})
    return True, f"Added {n}."

def remove_recipient(email):
    n = email.strip().lower()
    rs = list_recipients()
    t = next((r for r in rs if r.email == n), None)
    if not t: return False, "Email not found."
    if t.builtin: return False, "Built-in recipients cannot be removed."
    _save_raw({"recipients": [{"email": r.email, "schedule": r.schedule, "builtin": r.builtin} for r in rs if r.email != n]})
    return True, f"Removed {n}."

def recipients_for_slot(slot):
    rs = list_recipients()
    if slot == "morning": return [r.email for r in rs if r.schedule in ("both","morning_only")]
    return [r.email for r in rs if r.schedule in ("both","evening_only")]