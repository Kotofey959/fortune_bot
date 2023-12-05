"""
Выборка таблицы User.
"""

from db.user.sql import UserTemplate


def get_select_template(params: dict = None):
    """
    Возвращает пользователей по переданным параметрам.

    :param params: Параметры запроса, defaults to None
    :return: Список пользователей.
    """
    template = UserTemplate.select

    return template.render(params=params)