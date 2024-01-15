import asyncio
import sys
from typing import Any, Coroutine, TypeVar

_T = TypeVar("_T")


def run(coro: Coroutine[Any, Any, _T]) -> _T:
    try:
        import uvloop
    except (ImportError, RuntimeError):
        return asyncio.run(coro)

    if sys.version_info < (3, 11):
        uvloop.install()
        return asyncio.run(coro)

    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        return runner.run(coro)
