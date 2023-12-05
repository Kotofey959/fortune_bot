"""
Логика работы рулетки

"""
import asyncio
import random
from typing import Dict

from aiogram.types import CallbackQuery, InputFile, BufferedInputFile, FSInputFile

from button.main import Button
from button.user import REPEAT_SPIN
from keyboard.user import create_inline
from model.user import UserModel
from roulette.prizes import YOUR_PORTRAIT, NEW_YEAR, NEURO_REELS, PRIZE_LIST, FILE_IDS


async def start_spin(callback: CallbackQuery):
    """
    Прокрут рулетки

    :param callback:
    :return:
    """
    user_obj = UserModel(pk_id=callback.from_user.id)
    if user_obj.usage_spins < 1:
        prize = YOUR_PORTRAIT
    elif user_obj.usage_spins == 1:
        prize = NEW_YEAR
    elif user_obj.usage_spins == 2:
        prize = NEURO_REELS
    else:
        prize = random.choices(PRIZE_LIST, weights=[.3, .3, .3], k=1)[0]
    user_obj.change_spin_count(-1)
    user_obj.change_spin_usage_count(1)

    photo = FSInputFile(prize.get("photo"))
    answer_text = get_text_by_prize(prize)
    keyboard = create_inline(Button(text="Получить приз", callback=f"prize_{prize.get('file')}"),
                             REPEAT_SPIN)

    gif_message = await callback.message.answer_animation(FILE_IDS.get("gif"))
    await asyncio.sleep(3)
    await gif_message.delete()
    await callback.message.answer_photo(photo=photo, caption=answer_text, reply_markup=keyboard)
    await callback.answer()


def get_text_by_prize(prize: Dict):
    """
    Возвращает текст по переданному словарю приза

    :param prize:
    :return:
    """
    if not prize:
        return "В этот раз удача не на твоей стороне. Крутим еще раз?"
    return f"Поздравляем! Твой приз:\n\n" \
           f"{prize.get('title')}\n\n" \
           f"Крутим еще раз?"
