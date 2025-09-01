import asyncio
import logging
import os
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from dotenv import load_dotenv


def setup_logger():
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))

    # Rotating file handler
    fh = RotatingFileHandler(os.path.join(log_dir, 'bot.log'), maxBytes=1_000_000, backupCount=5, encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))

    # Avoid duplicate handlers on reruns
    logger.handlers.clear()
    logger.addHandler(ch)
    logger.addHandler(fh)


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
    try:
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
            except Exception:
                logging.exception("Unexpected error in polling")
                await asyncio.sleep(3)
                continue
            else:
                break
    finally:
        # Graceful shutdown
        try:
            await bot.session.close()
        except Exception:
            pass


if __name__ == '__main__':
    asyncio.run(main())
