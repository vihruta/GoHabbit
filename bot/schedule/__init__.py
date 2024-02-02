from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone


# Создайте планировщик
scheduler = AsyncIOScheduler()
scheduler.start()

tz = timezone('Europe/Moscow')  # Замените на нужный вам часовой пояс


