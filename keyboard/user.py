"""
Клавиаутры пользователей
"""
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from button.main import Button
from keyboard.constant import TWO_BUTTONS_IN_A_ROW


def create_inline(*args: Button, adjust: int = None):
    """
    Создание inline клавиатур.

    :param adjust: количество кнопок в ряду
    :param args: модели Button
    :return:
    """
    adjust = adjust or TWO_BUTTONS_IN_A_ROW
    builder = InlineKeyboardBuilder()
    for button in args:
        if not button:
            continue
        builder.row(
            button.inline if button.callback else button.inline_url
        )
    builder.adjust(adjust)
    return builder.as_markup(resize_keyboard=True)
