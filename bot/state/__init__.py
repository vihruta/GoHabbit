from typing import Any, Awaitable, Callable

from aiogram import types

from .groups import *


async def state_data_middleware(
    handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
    event: types.TelegramObject,
    data: dict[str, Any],
) -> Any:
    data["state_data"] = await data["state"].get_data()
    return await handler(event, data)
