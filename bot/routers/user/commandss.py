from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter, logic

from ...state import PromptState
from ...payments import youpay
from ...phrases import phrases, button_phrases
from . import router
from ... import markups
from ...payments.subscription import update_subscription, check_subscription
from ...payments.promocode import PromocodesInfo
from ...habit import habit_settings

import logging


@router.message(Command(commands=['faq']))  # Блок команд через слеш
async def faq_command_handler(message: types.Message):
    await message.answer(phrases.faq_text)


@router.message(Command(commands=['pay']))
async def pay_command_handler(message: types.Message):
    await message.answer(phrases.subscription_info)
    await message.answer("Выберите срок подписки: ",
                         reply_markup=markups.select_subscription_markup)


@router.message(Command(commands=['info']))
async def pay_command_handler(message: types.Message):
    expires_date = await check_subscription(message.from_user.id)
    if expires_date:
        formatted_date = expires_date.strftime("%Y-%m-%d")
        await message.answer(f"Дата окончания подписки: {formatted_date}")
    else:
        await message.answer("У вас нет активной подписки.")


@router.message(Command(commands=['habit']))
async def choose_habit(message: types.Message):
    await message.answer("Выберите привычку.",
                         reply_markup=markups.select_habit_markup)


@router.callback_query_handler()
async def check_payment(call: types.CallbackQuery):
    action, payment_id = call.data.split(':')
    if action == "check_payment":
        subscription_type = youpay.check_pay(payment_id)
        if subscription_type:
            await update_subscription(call.from_user.id, subscription_type)
            await call.message.answer(button_phrases.ButtonPhrases.
                                      subscription_confirm[subscription_type])
            await call.message.edit_reply_markup(reply_markup=None)
        else:
            await call.message.answer('Платеж не прошел!')


@router.message(F.text == button_phrases.ButtonPhrases.water)
async def handle_water_habit(message: types.Message, state: FSMContext):
    habit_type = "Water"
    await message.answer(phrases.water_first_answer)
    await state.update_data(habit_type=habit_type)
    await state.set_state(PromptState.waiting_for_date)


@router.message(logic.or_f(StateFilter(PromptState.waiting_for_date)))
async def handle_date_info(message: types.Message, state: FSMContext):
    habit_type = (await state.get_data()).get("habit_type")
    habit_date = message.text
    if await habit_settings.check_date(message.from_user.id,
                                       habit_date, habit_type):
        await message.answer(phrases.habit_date_accept)
    else:
        await message.answer(phrases.habit_date_error)


@router.message(
    F.text == button_phrases.ButtonPhrases.week_subscription)  # Блок с ответами на подписку
async def handle_week_subscription(message: types.Message):
    price = button_phrases.ButtonPhrases.week_price
    subscription_type = "week"
    payment_url, payment_id = youpay.create_payment(price)
    await message.answer(button_phrases.ButtonPhrases.payment_faq,
                         reply_markup=markups.ReplyKeyboardRemove())
    await message.answer("Вы выбрали недельную подписку.",
                         reply_markup=markups.payment_markup
                         (payment_url, payment_id, price))


@router.message(F.text == button_phrases.ButtonPhrases.month_subscription)
async def handle_month_subscription(message: types.Message):
    price = button_phrases.ButtonPhrases.month_price
    subscription_type = "month"
    payment_url, payment_id = youpay.create_payment(price)
    await message.answer(button_phrases.ButtonPhrases.payment_faq,
                         reply_markup=markups.ReplyKeyboardRemove())
    await message.answer("Вы выбрали месячную подписку.",
                         reply_markup=markups.payment_markup
                         (payment_url, payment_id, price))


@router.message(F.text == button_phrases.ButtonPhrases.quarter_subscription)
async def handle_quarter_subscription(message: types.Message):
    price = button_phrases.ButtonPhrases.quarter_price
    subscription_type = "quarter"
    payment_url, payment_id = youpay.create_payment(price)
    await message.answer(button_phrases.ButtonPhrases.payment_faq,
                         reply_markup=markups.ReplyKeyboardRemove())
    await message.answer("Вы выбрали подписку на квартал.",
                         reply_markup=markups.payment_markup
                         (payment_url, payment_id, price))


@router.message(
    F.text == button_phrases.ButtonPhrases.promocode_text)  # Блок промокодов
async def handle_quarter_subscription(message: types.Message,
                                      state: FSMContext):
    await message.answer('Введите промокод',
                         reply_markup=markups.ReplyKeyboardRemove())
    await state.set_state(PromptState.waiting_for_promo)


@router.message(logic.or_f(StateFilter(PromptState.waiting_for_promo)))
async def promo_entered(message: types.Message, state: FSMContext):
    promo = message.text
    if promo in PromocodesInfo.promocodes:
        await update_subscription(message.from_user.id, promo)
        await state.clear()
    else:
        await message.answer(phrases.promo_error)
