import logging, time
from pathlib import Path
from agent.scheduler import start_scheduler
LOG = Path(__file__).parent / "logs"; LOG.mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler(LOG/"scheduler.log", encoding="utf-8"), logging.StreamHandler()])
start_scheduler()
logging.info("Scheduler started (9 AM & 5 PM IST)")
while True: time.sleep(60)