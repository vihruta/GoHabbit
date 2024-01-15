import logging

from . import routers, state
from .core import bot, dispatcher
from .database import DatabaseService, bot_user_middleware
from .phrases import phrases
from .utils import loader, startup
from .utils.paths import ROOT_PATH
from .utils.services import ServiceMiddleware
from .utils.token_service import TokenService
from .schedule import ScheduleService


async def setup_services():
    await ServiceMiddleware.manager.register(
        DatabaseService(), TokenService()
    ).setup_all()


def setup_middleware():
    dispatcher.message.middleware.register(state.state_data_middleware)
    dispatcher.callback_query.middleware.register(state.state_data_middleware)

    dispatcher.message.outer_middleware.register(bot_user_middleware)
    dispatcher.callback_query.outer_middleware.register(bot_user_middleware)
    dispatcher.my_chat_member.outer_middleware.register(bot_user_middleware)

    services_middleware = ServiceMiddleware()
    dispatcher.message.middleware.register(services_middleware)
    dispatcher.callback_query.middleware.register(services_middleware)


@dispatcher.startup()
async def on_startup():
    me = await bot.get_me()
    print(phrases.bot_started.format(me=me))


@dispatcher.shutdown()
async def on_shutdown():
    await ServiceMiddleware.manager.dispose_all()


async def main():
    log_filename = str((ROOT_PATH / "logs.log").resolve())

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format=r"%(asctime)s %(levelname)s %(message)s",
    )

    setup_middleware()
    await setup_services()

    loader.import_routers()
    dispatcher.include_router(routers.root_router)

    used_update_types = dispatcher.resolve_used_update_types()
    await dispatcher.start_polling(bot, allowed_updates=used_update_types)


startup.run(main())
