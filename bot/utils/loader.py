import importlib
from pathlib import Path

from .paths import ROUTERS_PATH

ROUTER_PRIORITIES = (
    "admin",
    "user",
    "prompt",
)


def import_routers():
    router_paths = __get_sorted_router_paths()

    for router_path in router_paths:
        if router_path.is_file():
            importlib.import_module(__get_router_import_path(router_path))
        else:
            __import_handlers(router_path)


def __get_router_import_path(router_path: Path):
    return f"bot.routers.{router_path.stem}"


def __get_handler_import_path(handler_path: Path):
    router_import_path = __get_router_import_path(handler_path.parent)
    return f"{router_import_path}.{handler_path.stem}"


def __get_router_priority(router_name: str):
    if router_name in ROUTER_PRIORITIES:
        return ROUTER_PRIORITIES.index(router_name)

    return len(ROUTER_PRIORITIES)


def __get_sorted_router_paths():
    router_paths = filter(lambda p: "__" not in p.name, ROUTERS_PATH.glob("*"))
    return sorted(router_paths, key=lambda p: (__get_router_priority(p.stem), p.stem))


def __get_sorted_handler_paths(router_path: Path):
    handler_paths = filter(
        lambda p: "__" not in p.name and p.is_file(), router_path.glob("*.*")
    )

    return sorted(handler_paths, key=lambda p: p.stem)


def __import_handlers(router_path: Path):
    handler_paths = __get_sorted_handler_paths(router_path)

    for handler_filepath in handler_paths:
        importlib.import_module(__get_handler_import_path(handler_filepath))
