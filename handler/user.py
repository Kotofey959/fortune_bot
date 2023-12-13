"""
Хендлеры юзеров

"""
from asyncio import sleep

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import ChatMemberUpdated, CallbackQuery
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.utils.markdown import hlink

from button.user import SPIN
from db.main import database, LOGGER
from helper.referal import split_ref_link
from model.user import UserModel
from roulette.main import start_spin
from roulette.prizes import FILE_IDS
from text import NOT_AVAILABLE_SPINS, MAILING
from db.user.select import get_sharlatan_select_template as user_select

user_router = Router()


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


@user_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    """
    Обработка вступления нового пользователя в канал

    :param event:
    :return:
    """
    if event.invite_link:
        invite_link = split_ref_link(event.invite_link.invite_link)
        refferrer_user_obj = UserModel(ref_link=invite_link)
        refferrer_user_obj.change_spin_count(1)


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


@user_router.callback_query(F.data.startswith("prize"))
async def prize(callback: CallbackQuery):
    """
    Обрабатываем кнопку получить приз

    :param callback:
    :return:
    """
    file_id_key = callback.data.split("_")[1]
    file_id = FILE_IDS.get(file_id_key)
    if file_id.startswith("BAA"):
        await callback.message.reply_video(file_id)
    elif file_id.startswith("BQ"):
        await callback.message.reply_document(file_id)
    await callback.answer()
