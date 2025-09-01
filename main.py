import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


def setup_logger():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


async def main():
    load_dotenv()
    token = os.getenv('API_TOKEN')
    if not token:
        raise RuntimeError('API_TOKEN is not set in .env')

    setup_logger()

    bot = Bot(token=token)
    dp = Dispatcher()

    from bot.handlers.base import router as base_router
    dp.include_router(base_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
