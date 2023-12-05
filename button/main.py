"""
Кнопки инлайн клавиатур.
"""

from dataclasses import dataclass
from typing import Tuple

from aiogram.types import BotCommand, InlineKeyboardButton


@dataclass
class Button:
    """
    Стандартная кнопочка. Хранит в себе всю инфу для ее создания.
    """

    text: str
    callback: str = None
    url: str = None

    def as_tuple(self) -> Tuple:
        """
        Возвращает кнопку в виде тапла.
        """
        return (self.text, self.callback)

    @property
    def inline(self) -> InlineKeyboardButton:
        """
        Возвращает Inline кнопку.
        """
        return InlineKeyboardButton(text=self.text, callback_data=self.callback)

    @property
    def inline_url(self) -> InlineKeyboardButton:
        """
        Возвращает inline кнопку с URL
        :return:
        """
        return InlineKeyboardButton(text=self.text, url=self.url)


@dataclass
class Command(Button):
    """
    Кнопочка для команды в боте. Используются для кнопок над строкой ввода сообщения.
    """

    @property
    def command(self) -> BotCommand:
        """
        Возвращает команду для бота.
        """
        return BotCommand(command=self.callback, description=self.text)
