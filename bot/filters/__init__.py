from typing import Any

from aiogram import types

from .. import utils
from ..config import config
from ..core import bot
from ..database.models import BotUser
from ..phrases import phrases


def is_admin(user_id: int):
    return int(config.admin_user_id) == user_id


async def admin_filter(telegram_object: types.TelegramObject):
    from_user: types.User | None = getattr(telegram_object, "from_user", None)
    return from_user and is_admin(from_user.id)


async def access_filter(_: Any, bot_user: BotUser):
    if (
        bot_user.subscription_expires_at is not None
        and bot_user.subscription_expires_at > utils.utc_now()
    ):
        return True
    if bot_user.trial_requests_remaining > 0:
        bot_user.trial_requests_remaining -= 1
        await bot_user.save()
        return True

    await bot.send_message(bot_user.id, phrases.trial_end_text)
    return False