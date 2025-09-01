from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.dev_reload import DynamicRouterHolder


def get_admin_router(holder: DynamicRouterHolder) -> Router:
    router = Router(name='admin')

    @router.message(Command('reload'))
    async def reload_handlers(message: Message):
        holder.attach_fresh()
        await message.answer('Handlers reloaded')

    return router
