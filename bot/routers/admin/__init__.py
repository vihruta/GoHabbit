from ...filters import admin_filter
from ...utils.router import Router
from .. import root_router

router = Router()

router.message.filter(admin_filter)
router.callback_query.filter(admin_filter)
root_router.include_router(router)
