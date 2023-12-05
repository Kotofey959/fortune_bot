"""
Добавление записи в таблицу User.
"""

from db.user.sql import UserTemplate


def get_insert_template(
        telegram_id: int,
        ref_link: str,
        spin_available: int = 1,
        spin_usage: int = 0
):
    """
    Возвращает шаблон для вставки в таблицу пользователей.

    :param spin_usage:
    :param ref_link:
    :param spin_available:
    :param telegram_id: Идентификатор телеграма.
    :return: Срендеренный шаблон.
    """
    template = UserTemplate.insert
    context = {"telegram_id": telegram_id,
               "spin_available": spin_available,
               "spin_usage": spin_usage,
               "ref_link": ref_link}

    return template.render(context)
