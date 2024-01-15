from datetime import datetime, timedelta
from ..database.models import BotUser
from ..core import bot
from ..phrases import phrases
from ..schedule import jobs
import json


async def check_date(user_id, habit_date, habit_type):
    try:
        habit_date_list = habit_date.split(',')
        for date_str in habit_date_list:
            date_str_list = date_str.split(':')
            if len(date_str_list) == 2:
                hour, minute = int(date_str_list[0]), int(date_str_list[1])
                if 0 <= hour < 24 and 0 <= minute < 60:
                    pass
                else:
                    return False
            else:
                return False
    except (ValueError, IndexError):
        return False

    await add_date_to_database(user_id, habit_date_list, habit_type)
    return True


async def add_date_to_database(user_id, habit_date_list, habit_type):

    user = await BotUser.get(id=user_id)
    await user.set_habit_schedule(habit_type, habit_date_list)

    await bot.send_message(user_id, f'Время установлено для {habit_type}')

    habit_schedule_dict = json.loads(user.habit_schedule)
    await jobs.add_user_schedule(user_id, habit_schedule_dict)

