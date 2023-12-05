"""
Вспомогательные методы типов данных

"""
from typing import Any

from logger import get_logger

LOGGER = get_logger()


def to_int(value: Any) -> int | None:
    """
    Привести строку к int.
    :param value:
    :return:
    """
    result = None

    if not value:
        return result

    try:
        value = value.replace(" ", "") if isinstance(value, str) else value
        result = int(value)
    except Exception as ex:
        LOGGER.error(f"Не удалось привести строку к int: {ex}", exc_info=True)

    return result


def to_str(value: Any) -> str:
    """
    Очистить строку - удалить пробелы в начале и конце
    :param value:
    :return:
    """
    return str(value).strip() if value is not None else ""
