from aiogram import F, enums, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.filters.magic_data import MagicData

from .. import utils
from ..database.models import BotChat, BotUser
from ..utils.router import Router
from . import root_router

router = Router()
root_router.include_router(router)


@router.my_chat_member(
    F.chat.type == enums.ChatType.PRIVATE,
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER),
    MagicData(~F.is_new_bot_user),
)
async def joined_user_handler(_: types.ChatMemberUpdated, bot_user: BotUser):
    bot_user.joined_at = utils.utc_now()
    bot_user.left_at = None  # type: ignore
    await bot_user.save()


@router.my_chat_member(
    F.chat.type == enums.ChatType.PRIVATE,
    ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER),
)
async def left_user_handler(_: types.ChatMemberUpdated, bot_user: BotUser):
    bot_user.left_at = utils.utc_now()
    await bot_user.save()


@router.my_chat_member(
    F.chat.type != enums.ChatType.PRIVATE,
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER),
)
async def new_chat_handler(update: types.ChatMemberUpdated):
    await BotChat.update_or_create(
        dict(
            title=update.chat.title,
            username=update.chat.username,
            type=update.chat.type,
        ),
        id=update.chat.id,
    )


@router.my_chat_member(
    F.chat.type != enums.ChatType.PRIVATE,
    ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER),
)
async def removed_chat_handler(update: types.ChatMemberUpdated):
    await BotChat.filter(id=update.chat.id).delete()
