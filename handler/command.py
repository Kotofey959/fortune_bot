"""
Хендлеры команд

"""
from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from button.user import SPIN
from keyboard.user import create_inline
from model.user import UserModel
from text import MENU_START_TEXT

command_router = Router()


@command_router.message(CommandStart())
async def start(message: Message, state: FSMContext, bot: Bot):
    """
    Обработка команды старт.

    :param bot:
    :param state:
    :param message:
    :return:
    """
    await state.set_data({})
    telegram_id = message.from_user.id
    user_name = message.from_user.full_name

    user_obj = UserModel(telegram_id)
    text = MENU_START_TEXT.format(user_name)
    keyboard = create_inline(SPIN)
    if not user_obj.record:
        await user_obj.create(bot)

    await message.answer(text=text, reply_markup=keyboard)
