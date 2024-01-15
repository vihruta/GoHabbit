from aiogram.dispatcher.event.handler import CallbackType
from aiogram.dispatcher.router import Router as AiogramRouter


class Router(AiogramRouter):
    def filter(self, *filters: CallbackType) -> None:
        for observer in self.observers.values():
            observer.filter(*filters)

    def callback_query_handler(self, *custom_filters, **kwargs):
        def decorator(callback):
            self.callback_query.register(callback, *custom_filters, **kwargs)
            return callback
        return decorator
