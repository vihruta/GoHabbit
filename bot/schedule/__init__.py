from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone


# Создайте планировщик
scheduler = AsyncIOScheduler()
scheduler.start()

tz = timezone('UTC')  # Замените на нужный вам часовой пояс


