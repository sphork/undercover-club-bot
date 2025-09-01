import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
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

    while True:
        try:
            logging.info("Start polling")
            await dp.start_polling(bot)
        except TelegramNetworkError as e:
            logging.error(f"Polling error: {e}")
            await asyncio.sleep(2)
            continue
        except asyncio.CancelledError:
            logging.info("Polling cancelled")
            break
        except Exception as e:
            logging.exception("Unexpected error in polling")
            await asyncio.sleep(3)
            continue
        else:
            break


if __name__ == '__main__':
    asyncio.run(main())
