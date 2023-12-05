"""
Запуск бота.
"""
import asyncio

from loader import bot, dp
from handler.command import command_router
from handler.user import user_router
from logger import get_logger


LOGGER = get_logger()


async def main():
    """
    Запуск бота.

    :return:
    """
    LOGGER.info("Starting bot")

    dp.include_router(command_router)
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        LOGGER.error("Bot stopped!")
