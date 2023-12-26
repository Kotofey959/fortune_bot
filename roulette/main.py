"""
Логика работы рулетки

"""
import asyncio
import random
from typing import Dict

from aiogram.types import CallbackQuery, InputFile, BufferedInputFile, FSInputFile

from button.main import Button
from button.user import REPEAT_SPIN, SPIN
from keyboard.user import create_inline
from model.user import UserModel
from roulette.helper import get_prize_list, update_super_prize_count
from roulette.prizes import FILE_IDS
from text import FIRST_SPIN, SUPER_PRIZE


async def start_spin(callback: CallbackQuery):
    """
    Прокрут рулетки

    :param callback:
    :return:
    """
    user_obj = UserModel(pk_id=callback.from_user.id)
    if user_obj.usage_spins < 1:
        await callback.message.answer(text=FIRST_SPIN, reply_markup=create_inline(SPIN))
        await callback.answer()
        user_obj.change_spin_count(-1)
        user_obj.change_spin_usage_count(1)
        return
    prize_list = get_prize_list()
    prize = random.choice(prize_list)
    if prize.get("text"):
        await callback.message.answer(text=SUPER_PRIZE, reply_markup=create_inline(SPIN))
        await callback.answer()
        update_super_prize_count()
        user_obj.change_spin_count(-1)
        user_obj.change_spin_usage_count(1)
        return
    file_id = random.choice(FILE_IDS.get(prize.get("file")))
    answer_text = get_text_by_prize(prize)
    await callback.message.answer(text=answer_text)
    if file_id.startswith("AgA"):
        await callback.message.answer_photo(file_id, reply_markup=create_inline(SPIN))
    elif file_id.startswith("BQA"):
        await callback.message.answer_document(file_id, reply_markup=create_inline(SPIN))
    await callback.answer()

    user_obj.change_spin_count(-1)
    user_obj.change_spin_usage_count(1)


def get_text_by_prize(prize: Dict):
    """
    Возвращает текст по переданному словарю приза

    :param prize:
    :return:
    """

    return f"Поздравляем! Твой приз:\n\n" \
           f"{prize.get('title')}\n\n"
