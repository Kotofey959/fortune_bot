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
