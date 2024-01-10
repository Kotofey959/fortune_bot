"""
Хендлеры юзеров

"""
from asyncio import sleep

from aiogram import Router, F, Bot, types
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hlink

from button.user import SPIN, ROULETTE, START_CHAT
from db.main import database, LOGGER
from filters.main import ChatTypeFilter
from helper.list import get_first_elem
from keyboard.user import create_inline
from model.user import UserModel
from roulette.main import start_spin
from text import NOT_AVAILABLE_SPINS, MAILING, ROULETTE_START_TEXT
from db.user.select import get_sharlatan_select_template as user_select
from db.messages.insert import get_insert_template as message_insert
from db.messages.select import get_select_template as message_select

user_router = Router()


class UserState(StatesGroup):
    """
    Состояния пользователя.

    """

    wait_question = State()


@user_router.message()
async def test(message: Message):
    if message.video:
        await message.answer(message.video.file_id)


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

    await callback.message.answer_video(
        video="BAACAgIAAxkBAAInn2WMQTvwzqv2hcG_lz2U3X8V39zjAAJfOQACho5gSI7jccicZ51rMwQ",
        caption=text,
        reply_markup=keyboard)
    await callback.answer()


# @user_router.callback_query(F.data == SPIN.callback)
# async def spin(callback: CallbackQuery):
#     """
#     Обрабатываем кнопку Крутить колесо фортуны
#
#     :param callback:
#     :return:
#     """
#     user_obj = UserModel(callback.from_user.id)
#     if user_obj.available_spins < 1:
#         answer_text = NOT_AVAILABLE_SPINS.format(user_obj.ref_link)
#         await callback.message.answer(text=answer_text)
#         await callback.answer()
#         return
#
#     await start_spin(callback)


@user_router.callback_query(F.data == START_CHAT.callback)
async def start_chat(callback: CallbackQuery, state: FSMContext):
    """

    :param state:
    :param callback:
    :return:
    """
    await state.set_state(UserState.wait_question)
    await callback.message.answer("Напишите свой вопрос. Консультант ответит вам в ближайшее время.")
    await callback.answer()


@user_router.message(UserState.wait_question, F.text)
async def wait_question(message: Message, state: FSMContext, bot: Bot):
    """

    :param bot:
    :param message:
    :param state:
    :return:
    """
    await state.clear()
    await message.answer("Ваш вопрос отправлен консультанту.")
    forwarded_message = await bot.forward_message(chat_id=-1002083730072, from_chat_id=message.chat.id, message_id=message.message_id)
    user_id = message.from_user.id
    message_id = message.message_id
    forwarded_message_id = forwarded_message.message_id
    template = message_insert(user_id, message_id, forwarded_message_id)
    database.execute(template)


@user_router.message(ChatTypeFilter(chat_type=["group", "supergroup"]))
async def wait_answer(message: Message, bot: Bot):
    """

    :param message:
    :param bot:
    :return:
    """
    if not message.reply_to_message:
        return
    template = message_select({"forwarded_message_id": message.reply_to_message.message_id})
    sql_res = database.select_as_dict(template)
    result = get_first_elem(sql_res)
    if result:
        await bot.send_message(result.get("user_id"),
                               message.text,
                               reply_to_message_id=result.get("message_id"))