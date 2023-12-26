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
from roulette.prizes import FILE_IDS
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

    user_obj = UserModel(telegram_id)
    if not user_obj.record:
        await user_obj.create(bot)
    available_spins = user_obj.available_spins
    print(available_spins)
    text = MENU_START_TEXT.format(available_spins)
    keyboard = create_inline(SPIN)

    await message.answer_photo(photo="AgACAgIAAxkBAAIjPWWKz7znaOz-V9x8OVeauexN_r-OAAJA0DEbIAFYSFg0xSZ4ovdyAQADAgADcwADMwQ",
                               text=text,
                               reply_markup=keyboard)
