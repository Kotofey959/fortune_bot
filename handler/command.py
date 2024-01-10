"""
Хендлеры команд

"""
from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from button.user import START_CHAT, ROULETTE
from helper.string import get_ref_id
from keyboard.user import create_inline
from model.user import UserModel
from text import MENU_START_TEXT, NEW_REFERRAL

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
    await state.clear()
    new_user_obj = UserModel(int(message.from_user.id))
    if not new_user_obj.record:
        await new_user_obj.create(bot)
        ref_id = get_ref_id(message.text)
        if ref_id is not None:
            user_obj = UserModel(ref_id or 0)
            user_obj.change_spin_count(1)
            answer_text = NEW_REFERRAL.format(user_obj.available_spins)
            await bot.send_message(ref_id, answer_text)
    keyboard = create_inline(START_CHAT, adjust=1)
    await message.answer(text=MENU_START_TEXT, reply_markup=keyboard)
