from aiogram import Bot

from button.command import START_COMMAND


async def set_bot_command(bot: Bot):
    """
    Устанавливает команды в бота.
    """
    commands = [
        START_COMMAND.command
    ]

    await bot.set_my_commands(commands)