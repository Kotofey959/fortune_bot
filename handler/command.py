"""
Хендлеры команд

"""
from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from button.user import SPIN, START_CHAT, ROULETTE
from keyboard.user import create_inline
from model.user import UserModel
from roulette.prizes import FILE_IDS
from text import MENU_START_TEXT

command_router = Router()


@command_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    """
    Обработка команды старт.

    :param state:
    :param message:
    :return:
    """
    await state.clear()
    keyboard = create_inline(ROULETTE, START_CHAT, adjust=1)
    await message.answer(text=MENU_START_TEXT, reply_markup=keyboard)
