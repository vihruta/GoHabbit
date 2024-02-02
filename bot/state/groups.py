from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup

from ..utils.token_service import ContextRecord


class PromptState(StatesGroup):
    class Data(TypedDict):
        context_records: list[ContextRecord]

    waiting_question = State()
    waiting_answer = State()
    waiting_for_promo = State()
    waiting_for_date = State()
    waiting_for_habit = State()
