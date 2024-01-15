from datetime import datetime, timedelta
from ..database.models import BotUser
from ..core import bot
from ..phrases import phrases

from . import promocode


async def update_subscription(user_id, subscription_duration):
    user = await BotUser.get(id=user_id)

    user.subscription_started_at = datetime.now()

    if subscription_duration == "week":
        user.subscription_expires_at = datetime.now() + timedelta(weeks=1)
    elif subscription_duration == "month":
        user.subscription_expires_at = datetime.now() + timedelta(weeks=4)
    elif subscription_duration == "quarter":
        user.subscription_expires_at = datetime.now() + timedelta(weeks=12)
    if subscription_duration in promocode.PromocodesInfo.promocodes:
        date_expires = promocode.PromocodesInfo.promocode_date[subscription_duration]
        if check_date(date_expires):
            user.subscription_expires_at =\
                datetime(date_expires[0], date_expires[1], date_expires[2])
        else:
            await bot.send_message(user_id, phrases.promo_error)
            return

    formatted_date = user.subscription_expires_at.strftime("%d-%m-%Y")
    await bot.send_message(user_id, phrases.promo_confirm + formatted_date)
    await user.save()


async def check_subscription(user_id):
    user = await BotUser.get(id=user_id)
    expires_date = user.subscription_expires_at
    return expires_date


def check_date(date_list):
    date_expires = datetime(*date_list).date()
    today = datetime.now().date()
    if date_expires > today:
        return True
    else:
        return False

