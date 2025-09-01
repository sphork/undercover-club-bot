import importlib
from typing import Optional
from aiogram import Router


class DynamicRouterHolder:
    """Holds a child router that can be swapped at runtime."""

    def __init__(self) -> None:
        self.root = Router(name='dynamic_root')
        self._child: Optional[Router] = None

    def load_handlers(self) -> Router:
        module = importlib.import_module('bot.handlers.base')
        # Reload module to apply code changes during dev
        module = importlib.reload(module)
        return module.router

    def attach_fresh(self) -> None:
        # Remove previous child router if exists
        if self._child and self._child in self.root.children:
            try:
                self.root.children.remove(self._child)
            except ValueError:
                pass
        # Load and attach a fresh router
        self._child = self.load_handlers()
        self.root.include_router(self._child)
