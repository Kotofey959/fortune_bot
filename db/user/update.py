"""
Обновление записи в таблицее User.
"""

from db.user.sql import UserTemplate


def get_update_spin_available_template(telegram_id: int, count_spin=1):
    """
    Устанавливает количество доступных прокрутов

    :param count_spin:
    :param telegram_id: Идентификатор телеграма.
    :return: Срендеренный шаблон.
    """
    if not telegram_id:
        return None

    template = UserTemplate.update_spin_available
    context = {"telegram_id": telegram_id, "count_spin": count_spin}

    return template.render(context=context)


def get_update_spin_usage_template(telegram_id: int, count_spin=1):
    """
    Устанавливает количество использованных прокрутов

    :param count_spin:
    :param telegram_id: Идентификатор телеграма.
    :return: Срендеренный шаблон.
    """
    if not telegram_id:
        return None

    template = UserTemplate.update_spin_usage
    context = {"telegram_id": telegram_id, "count_spin": count_spin}

    return template.render(context=context)
