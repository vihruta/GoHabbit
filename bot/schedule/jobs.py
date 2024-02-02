import json

from pytz import timezone
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext


from ..core import bot
import logging
from ..schedule import scheduler
from ..routers import prompt
from ..habit import habit_settings
from .. import markups
from ..database.models import BotUser

tz = timezone('Europe/Moscow')


async def send_reminder(user_id, habit_type, state: FSMContext = None):
    try:
        logging.info(
            f"Начинаем отправку напоминания для пользователя {user_id} о привычке {habit_type}")
        prompt_text = habit_settings.choose_prompt_for_habit(habit_type)
        try:
            response_text = prompt.generate_response_with_chatgpt(prompt_text)
            if response_text:
                if state:
                    await state.update_data(habit_type=habit_type)
                await bot.send_message(user_id, response_text)
                await bot.send_message(user_id, "Сделано?",
                                       reply_markup=markups.confirm_action_markup)
            else:
                await bot.send_message(user_id, 'Ошибка генерации')
            logging.info(
                f"Напоминание отправлено пользователю {user_id} о привычке {habit_type}")
        except Exception as e:
            logging.error(f"Ошибка при отправке напоминания: {e}")
    except Exception as e:
        logging.info(f'Ошибка при запуске send_reminder: {e}')


async def add_user_schedule(*args):
    user_id = args[0]
    if len(args) == 3:
        reminder_data = args[1] + 'Reminder'
        five_minutes_later = datetime.now(tz) + timedelta(minutes=5)
        scheduler.add_job(send_reminder, 'date', run_date=five_minutes_later,
                          args=[user_id, reminder_data], timezone=tz)
    else:
        reminder_data = args[1]
        for habit_type, times in reminder_data.items():
            for time in times:
                # logging.info(f'{user_id},{habit_type}')
                # logging.info(f'Настройкая для времени {time}')
                hours, minutes = map(int, time.split(':'))
                current_time = datetime.now().astimezone(tz)
                # Задайте время выполнения задачи, добавив текущее время и время из reminder_data
                execution_time = current_time.replace(hour=hours,
                                                      minute=minutes,
                                                      second=0, microsecond=0)
                # Если указанное время в будущем, добавьте задачу
                if execution_time <= current_time:
                    execution_time = execution_time + timedelta(days=1)

                    # Добавьте задачу с типом 'cron' для выполнения каждый день в указанное время
                try:
                    scheduler.add_job(send_reminder, 'cron',
                                      args=[user_id, habit_type], hour=hours,
                                      minute=minutes, timezone=tz)
                    logging.info(f'User: {user_id}, habit: {habit_type}, time: {hours}:{minutes}')
                except Exception as e:
                    logging.error(f'Ошибка при добавление в расписание: {e}')
                    pass


async def setup_habit_schedules():
    # Получаем пользователей, у которых есть ненулевое расписание привычек
    users = await BotUser.filter(habit_schedule__isnull=False).all()
    for user in users:
        user_id = user.id
        habit_schedule = user.habit_schedule
        if isinstance(habit_schedule, str):
            habit_schedule = json.loads(habit_schedule)
        elif not isinstance(habit_schedule, dict):
            continue
        user_id = user.id
        await add_user_schedule(user_id, habit_schedule)
