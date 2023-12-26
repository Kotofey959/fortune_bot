"""
Хендлеры юзеров

"""
from asyncio import sleep

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hlink

from button.user import SPIN, ROULETTE
from db.main import database, LOGGER
from keyboard.user import create_inline
from model.user import UserModel
from roulette.main import start_spin
from text import NOT_AVAILABLE_SPINS, MAILING, ROULETTE_START_TEXT
from db.user.select import get_sharlatan_select_template as user_select

user_router = Router()


@user_router.message()
async def get_file_id(message: Message):
    """
    Получение файлов документов

    :param message:
    :return:
    """
    if message.photo:
        await message.answer(message.photo[0].file_id)
    if message.document:
        await message.answer(message.document.file_id)
    if message.animation:
        await message.answer(message.animation.file_id)


@user_router.message(F.text == "саламчик")
async def mailing(message, bot: Bot):
    """
    Тестовый хендлер

    :param bot:
    :return:
    """
    sql_template = user_select()
    user_list = database.select_as_dict(sql_template)
    link = hlink("Получить бесплатный VPN", "https://t.me/oblivion_vpn_bot?start=193489837")
    for user in user_list:
        telegram_id = user.get("telegram_id")
        try:
            await bot.send_message(chat_id=telegram_id, text=MAILING)
            await sleep(0.05)
            await bot.send_message(chat_id=telegram_id, text=link)
            await sleep(0.05)
            LOGGER.info(f"Отправили сообщение пользователю {telegram_id}")
        except TelegramForbiddenError:
            continue


@user_router.callback_query(F.data == ROULETTE.callback)
async def start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обработка команды старт.

    :param callback:
    :param bot:
    :param state:
    :return:
    """
    await state.clear()
    telegram_id = callback.from_user.id

    user_obj = UserModel(telegram_id)
    if not user_obj.record:
        await user_obj.create(bot)
    available_spins = user_obj.available_spins
    text = ROULETTE_START_TEXT.format(available_spins)
    keyboard = create_inline(SPIN)

    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIjPWWKz7znaOz-V9x8OVeauexN_r-OAAJA0DEbIAFYSFg0xSZ4ovdyAQADAgADcwADMwQ",
        caption=text,
        reply_markup=keyboard)
    await callback.answer()


@user_router.callback_query(F.data == SPIN.callback)
async def spin(callback: CallbackQuery):
    """
    Обрабатываем кнопку Крутить колесо фортуны

    :param callback:
    :return:
    """
    user_obj = UserModel(callback.from_user.id)
    if user_obj.available_spins < 1:
        answer_text = NOT_AVAILABLE_SPINS.format(user_obj.ref_link)
        await callback.message.answer(text=answer_text)
        await callback.answer()
        return

    await start_spin(callback)
