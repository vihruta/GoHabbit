import asyncio
import itertools
import logging

import os

import openai
from aiogram import F, enums, types
from aiogram.filters import StateFilter, logic
from aiogram.fsm.context import FSMContext
from openai.error import InvalidRequestError, RateLimitError, Timeout
from openai.openai_object import OpenAIObject

from .. import filters
from ..config import config
from ..core import bot
from ..phrases import phrases
from ..state import PromptState
from ..utils.router import Router
from ..utils.token_service import ContextRecord, TokenService
from . import root_router

import time

MAX_CONTEXT_LEN = 10
MAX_RETRIES = 3

router = Router()
router.message.filter(filters.access_filter)
root_router.include_router(router)

api_keys = itertools.cycle(config.openai_api_keys)


# @router.message(
#     F.text, logic.or_f(StateFilter(None), StateFilter(PromptState.waiting_question))
# )
# async def question_handler(
#     message: types.Message,
#     state: FSMContext,
#     state_data: PromptState.Data,
#     token_service: TokenService,
# ):
#     logging.info(f"Начало обработки сообщения: {time.time()}")
#     await state.set_state(PromptState.waiting_answer)
#
#     context_records = state_data.get("context_records", [])
#
#     if (
#         len(context_records) >= MAX_CONTEXT_LEN
#         or token_service.count_context_tokens_count(context_records)
#         >= token_service.MAX_CONTEXT_TOKENS_COUNT
#     ):
#         context_records.clear()
#         await message.answer(phrases.context_cleanup_message_text)
#
#     current_context_record: ContextRecord = {# type: ignore
#         "content": message.text,
#         "role": "user",
#     }
#
#     context_records.append(current_context_record)
#     tokens_count = token_service.count_context_tokens_count(context_records)
#
#     retry_count = 0
#
#     completion = None
#
#     while retry_count < MAX_RETRIES:
#         typing_task = asyncio.create_task(keep_typing(message))
#         try:
#             current_api_key = next(api_keys)
#             openai.api_key = current_api_key
#             logging.info(f"Начало запроса к OpenAI: {time.time()}")
#             completion: OpenAIObject = await openai.ChatCompletion.acreate(  # type: ignore
#                 model="gpt-3.5-turbo",
#                 messages=context_records,
#                 max_tokens=token_service.MAX_CONTEXT_TOKENS_COUNT - tokens_count,
#             )
#             logging.info(f"Завершение запроса к OpenAI: {time.time()}")
#
#         except RateLimitError as e:
#             logging.error(e, exc_info=True)
#             await asyncio.sleep(e.retry_after)
#             retry_count += 1
#
#         except (InvalidRequestError, Timeout) as e:
#             logging.error(e, exc_info=True)
#             retry_count += 1
#             if isinstance(e, RateLimitError):
#                 await asyncio.sleep(e.retry_after)
#
#         except Timeout as e:
#             logging.error(e, exc_info=True)
#             await message.answer("Произошла ошибка, попробуйте повторить запрос.")
#             continue
#
#         except Exception as e:
#             logging.error(f"Неожиданная ошибка: {e}", exc_info=True)
#             await message.answer("Произошла ошибка, попробуйте повторить запрос.")
#             await state.clear()
#             raise e
#
#         else:
#             if completion is not None:
#                 break
#
#         finally:
#             await asyncio.sleep(0)
#             typing_task.cancel()
#
#     if retry_count >= MAX_RETRIES:
#         await message.answer(phrases.retry_limit_exceeded_message_text)
#         return
#
#     if completion is not None:
#         choice = completion.choices[0]
#         clean_content = token_service.clean_message_content(
#             choice.message.content)
#         context_records.append({"role": "assistant", "content": clean_content})
#         await message.answer(clean_content)
#         await state.update_data(context_records=context_records)
#         await state.set_state(PromptState.waiting_question)
#     logging.info(f"Конец обработки сообщения: {time.time()}")


@router.message(F.content_type != enums.ContentType.TEXT)
async def not_text_message_handler(message: types.Message):
    await message.answer(phrases.invalid_content_type_message_text)


# async def keep_typing(message: types.Message, interval: float = 5.0):
#     while True:
#         await bot.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
#         await asyncio.sleep(interval)


async def send_habbit_reminder(user_id, habit_type):
    await bot.send_message(user_id, f'Пора выпить воды! {habit_type}')
