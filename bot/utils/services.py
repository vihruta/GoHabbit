import asyncio
import re
from typing import Any, Awaitable, Callable, Dict, Protocol

from aiogram import BaseMiddleware, types


def _to_snake_case(string: str) -> str:
    return "_".join(
        re.sub(
            "([A-Z][a-z]+)",
            r" \1",
            re.sub("([A-Z]+)", r" \1", string.replace("-", " ")),
        ).split()
    ).lower()


class Service(Protocol):
    async def setup(self) -> Any:
        ...

    async def dispose(self) -> Any:
        ...


class ServiceManager:
    def __init__(self):
        self._services: dict[str, Service] = {}

    def _register(self, service: Service):
        service_class_snake_name = _to_snake_case(service.__class__.__name__)
        self._services[service_class_snake_name] = service
        return self

    def register(self, *services: Service):
        for service in services:
            self._register(service)

        return self

    def unregister(self, service: Service):
        service_class_snake_name = _to_snake_case(service.__class__.__name__)
        del self._services[service_class_snake_name]

    async def setup_all(self):
        if not self._services:
            return

        service_setup_coros = (service.setup() for service in self._services.values())
        await asyncio.gather(*service_setup_coros)

    async def dispose_all(self):
        if not self._services:
            return

        service_dispose_coros = (
            service.dispose() for service in self._services.values()
        )

        await asyncio.gather(*service_dispose_coros)


class ServiceMiddleware(BaseMiddleware):
    manager = ServiceManager()

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data.update(self.manager._services)
        return await handler(event, data)
