"""
Выборка таблицы User.
"""

from db.messages.sql import MessagesTemplate


def get_select_template(params: dict = None):
    """
    Возвращает пользователей по переданным параметрам.

    :param params: Параметры запроса, defaults to None
    :return: Список пользователей.
    """
    template = MessagesTemplate.select

    return template.render(params)