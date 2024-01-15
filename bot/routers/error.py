﻿import logging

from ..utils.router import Router
from . import root_router

router = Router()
root_router.include_router(router)


@router.errors()
async def errors_handler(error: Exception):
    logging.error(error, exc_info=True)
