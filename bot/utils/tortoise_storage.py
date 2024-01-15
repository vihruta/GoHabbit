from typing import Any

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

from ..database.models import StateBucket


class TortoiseStorage(BaseStorage):
    async def _update_or_create_bucket(
        self, key: StorageKey, defaults: dict[str, Any] | None = None
    ):
        return await StateBucket.update_or_create(
            defaults, bot_id=key.bot_id, chat_id=key.chat_id, user_id=key.user_id
        )

    async def set_state(self, key: StorageKey, state: StateType = None):
        _state = state.state if isinstance(state, State) else state
        return await self._update_or_create_bucket(key, dict(state=_state))

    async def get_state(self, key: StorageKey):
        bucket = await StateBucket.get_or_none(
            bot_id=key.bot_id, chat_id=key.chat_id, user_id=key.user_id
        )

        if bucket is None:
            return None

        return bucket.state

    async def set_data(self, key: StorageKey, data: dict[str, Any]):
        await self._update_or_create_bucket(key, dict(data=data))

    async def get_data(self, key: StorageKey):
        bucket, _ = await self._update_or_create_bucket(key)
        return bucket.data

    async def close(self):
        return
