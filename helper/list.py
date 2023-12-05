"""
Вспомогательные методы для работы со списком

"""
from typing import List, Any

from logger import get_logger

LOGGER = get_logger()


def get_elem(value: List[Any], index: int, default_value=None) -> Any:
    """
    Возвращает элемент списка по индексу.

    :param value: Список элементов
    :param index: Индекс искомого элемента
    :return: Элемент с индексом.
    """
    if default_value is None:
        default_value = {}

    element = default_value
    try:
        element = value[index]
    except Exception as ex:
        LOGGER.exception(f"Ошибка получения значения c индексом {index} из {value}: {ex}")
        element = default_value

    return element


def get_first_elem(value: List[Any], default_value=None):
    """
    Возвращает первый элемент списка.

    :param value: Список
    :param default_value: Стандартное значение List[Any], defaults to None
    """
    return get_elem(value, 0, default_value=default_value)
