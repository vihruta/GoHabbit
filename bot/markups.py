from aiogram import types
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from . import filters
from .phrases import phrases
from .phrases import button_phrases

remove_markup = types.ReplyKeyboardRemove(remove_keyboard=True)

admin_markup = (
    ReplyKeyboardBuilder()
    .button(text=phrases.admin.give_access_button_text)
    .button(text=phrases.admin.remove_access_button_text)
    .adjust(2, repeat=True)
    .as_markup(resize_keyboard=True)
)

select_user_markup = (
    ReplyKeyboardBuilder()
    .button(
        text=phrases.admin.select_user_button_text,
        request_user=types.KeyboardButtonRequestUser(request_id=1,
                                                     user_is_bot=False),
    )
    .as_markup(resize_keyboard=True)
)

select_subscription_markup = (
    ReplyKeyboardBuilder()
    .row(KeyboardButton(text=button_phrases.ButtonPhrases.week_subscription))
    .row(KeyboardButton(text=button_phrases.ButtonPhrases.month_subscription))
    .row(KeyboardButton(text=button_phrases.ButtonPhrases.quarter_subscription))
    .row(KeyboardButton(text=button_phrases.ButtonPhrases.promocode_text))
    .as_markup(resize_keyboard=True)
)

select_habit_markup = (
    ReplyKeyboardBuilder()
    .row(
        KeyboardButton(text=button_phrases.ButtonPhrases.water),
        KeyboardButton(text=button_phrases.ButtonPhrases.sleep),
        KeyboardButton(text=button_phrases.ButtonPhrases.drugs),
    )
    .as_markup(resize_keyboard=True)
)

confirm_action_markup = (
    InlineKeyboardBuilder()
    .row(
        InlineKeyboardButton(text=button_phrases.ButtonPhrases.confirmation,
                             callback_data='yes'),
        InlineKeyboardButton(text=button_phrases.ButtonPhrases.decline,
                             callback_data='no')
    )
    .as_markup(resize_keyboard=True)
)


def payment_markup(url, payment_id, price):
    payment_mark_up = (
        InlineKeyboardBuilder()
        .row(InlineKeyboardButton(text=(button_phrases.ButtonPhrases.pay_text
                                        + ' ' + price + ' RUB'),
                                  url=url))
        .row(InlineKeyboardButton(text=button_phrases.ButtonPhrases.pay_check,
                                  callback_data=f"check_payment:{payment_id}"))
        .as_markup(resize_keyboard=True)
    )
    return payment_mark_up


def get_start_markup(user_id: int):
    if filters.is_admin(user_id):
        return admin_markup

    return None
