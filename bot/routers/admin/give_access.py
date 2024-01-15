import datetime

from aiogram import F, types
from aiogram3_form import Form, FormField
from aiogram.fsm.context import FSMContext

from ... import markups, utils
from ...core import bot
from ...database.models import BotUser
from ...phrases import phrases
from . import router


async def bot_user_form_field_filter(message: types.Message):
    if not message.user_shared:
        return False

    bot_user = await BotUser.get_or_none(id=message.user_shared.user_id)

    if bot_user is None:
        return False

    return bot_user


BOT_USER_FORM_FIELD = FormField(
    enter_message_text=phrases.admin.select_user_message_text,
    filter=bot_user_form_field_filter,
    error_message_text=phrases.admin.bot_user_not_found_message_text,
    reply_markup=markups.select_user_markup,
)


class GiveAccessForm(Form, router=router):
    bot_user: BotUser = BOT_USER_FORM_FIELD
    access_expires_at: datetime.datetime = FormField(
        enter_message_text=phrases.admin.enter_access_expires_at_datetime_message_text
    )


@GiveAccessForm.submit()
async def give_access_form_submit_handler(form: GiveAccessForm):
    form.bot_user.subscription_expires_at = form.access_expires_at.astimezone(
        datetime.timezone.utc
    )
    form.bot_user.subscription_started_at = utils.utc_now()
    await form.bot_user.save()
    await form.answer(
        phrases.admin.give_access_message_text, reply_markup=markups.admin_markup
    )


@router.message(F.text == phrases.admin.give_access_button_text)
async def give_access_handler(_: types.Message, state: FSMContext):
    await GiveAccessForm.start(bot, state)
