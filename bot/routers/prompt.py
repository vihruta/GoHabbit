import asyncio
import itertools
import logging

import os

import openai
from aiogram import F, enums, types
from transformers import GPT2Tokenizer

from .. import filters
from ..core import bot
from ..phrases import phrases
from ..utils.router import Router
from . import root_router


router = Router()
# router.message.filter(filters.access_filter)
root_router.include_router(router)

api_key = "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"


def generate_response_with_chatgpt(prompt_text: str):
    openai.api_key = api_key
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Вы чат-бот, помогающий людям поддерживать полезные привычки."},
                {"role": "user", "content": prompt_text},
            ]
        )

        response_text = response.choices[0].message.content
        prompt_tokens = len(tokenizer.encode(prompt_text))
        response_tokens = len(tokenizer.encode(response_text))
        total_tokens = prompt_tokens + response_tokens
        logging.info(f'Количество использованных токенов: {total_tokens}')

        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Ошибка при запросе к OpenAI: {e}")
        return None


@router.message(F.content_type != enums.ContentType.TEXT)
async def not_text_message_handler(message: types.Message):
    await message.answer(phrases.invalid_content_type_message_text)


async def keep_typing(message: types.Message, interval: float = 5.0):
    while True:
        await bot.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await asyncio.sleep(interval)
