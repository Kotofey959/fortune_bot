"""
Вспомогательные методы строки

"""
import re

from helper.datatype import to_str


def remove_spaces(text: str) -> str:
    """
    Удаляет лишние пробелы из строки.

    :param text: Строка с кучей пробелов
    :return: Строка с минимумом пробелов
    """
    return re.sub(' +', ' ', to_str(text))


def get_ref_id(link: str) -> int or None:
    """
    Достаем из переданной ссылки id рефера

    """
    link_split = link.split("=")
    if len(link_split) == 2 and link_split[1].isdigit():
        return int(link_split[1])
    return None
