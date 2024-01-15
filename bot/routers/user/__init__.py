from ...utils.router import Router
from .. import root_router

router = Router()
root_router.include_router(router)
