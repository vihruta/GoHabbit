import logging

from ..database.models import BotUser
from ..schedule import jobs
import json
from ..phrases import phrases_for_prompt


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

    habit_schedule_dict = json.loads(user.habit_schedule)
    await jobs.add_user_schedule(user_id, habit_schedule_dict)


async def get_habit_list(user_id):
    user = await BotUser.get(id=user_id)
    if user.habit_schedule and isinstance(user.habit_schedule, str):
        habit_schedule = json.loads(user.habit_schedule)
    else:
        habit_schedule = user.habit_schedule or {}
    return habit_schedule


def choose_prompt_for_habit(habit_type):
    if 'Water' in habit_type:
        if 'Reminder' in habit_type:
            return phrases_for_prompt.PromptPhrases.water_reminder
        return phrases_for_prompt.PromptPhrases.water
    if 'Sleep' in habit_type:
        if 'Reminder' in habit_type:
            return phrases_for_prompt.PromptPhrases.sleep_reminder
        return phrases_for_prompt.PromptPhrases.sleep
    if habit_type == 'Drugs':
        return phrases_for_prompt.PromptPhrases.drugs


def check_timezone():
    pass

