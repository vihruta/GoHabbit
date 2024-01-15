from aiogram import types
from aiogram.filters.command import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from ... import markups
from ...phrases import phrases
from . import router


@router.message(CommandStart())
async def start_command_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        phrases.start_message_text,
        reply_markup=markups.get_start_markup(message.chat.id),
    )


