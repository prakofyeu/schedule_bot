from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import send_schedule_for_day

scheduler = AsyncIOScheduler()

def start_scheluder():
    scheduler.add_job(send_schedule_for_day, "cron", hour=21, minute=0)
    scheduler.start()