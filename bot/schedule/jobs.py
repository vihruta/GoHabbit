from ..core import bot
import aioschedule
import asyncio
from datetime import datetime
from ..routers import prompt


async def add_user_schedule(user_id, reminder_data):
    for habit_type, times in reminder_data.items():
        for time in times:
            # Разбираем время из строки и создаем объект datetime
            hour, minute = map(int, time.split(':'))
            scheduled_time = datetime.now().replace(hour=hour,
                                                    minute=minute,
                                                    second=0,
                                                    microsecond=0)
            aioschedule.every().day.at(scheduled_time.strftime("%H:%M")).do(
                lambda: asyncio.create_task(send_scheduled_reminder(user_id, habit_type)))


async def send_scheduled_reminder(user_id, habit_type):
    await prompt.send_habbit_reminder(user_id, habit_type)
