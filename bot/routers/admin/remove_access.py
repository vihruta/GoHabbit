from aiogram import F, types
from aiogram3_form import Form
from aiogram.fsm.context import FSMContext

from ... import markups
from ...core import bot
from ...database.models import BotUser
from ...phrases import phrases
from . import router
from .give_access import BOT_USER_FORM_FIELD


class RemoveAccessForm(Form, router=router):
    bot_user: BotUser = BOT_USER_FORM_FIELD


@RemoveAccessForm.submit()
async def remove_access_form_submit_handler(form: RemoveAccessForm):
    form.bot_user.subscription_expires_at = None  # type: ignore
    await form.bot_user.save()
    await form.answer(
        phrases.admin.remove_access_message_text, reply_markup=markups.admin_markup
    )


@router.message(F.text == phrases.admin.remove_access_button_text)
async def remove_access_handler(_: types.Message, state: FSMContext):
    await RemoveAccessForm.start(bot, state)
