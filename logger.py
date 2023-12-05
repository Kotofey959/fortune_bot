"""
Логгер для функций.
"""

import logging

from datetime import datetime
from http.client import HTTPConnection
from pathlib import Path
from typing import ParamSpec, TypeVar

from helper.datetime import date_to_str

CALL_BEGIN = 'Вызов метода "{method}".'
CALL_ERROR = 'Ошибка при выполнении "{method}":\n\r{trace}'
CALL_RESULT = 'Метод "{method}" выполнен за "{time}" ms.'

P = ParamSpec("P")
T = TypeVar("T")

LOG_FILE_NAME = f"{date_to_str(datetime.now())}.log"
LOG_FOLDER = "logs"
LOG_ENCODING = "utf-8"
LOG_PATH = Path(Path.cwd() / LOG_FOLDER)


def _init_logger():
    """
    Инициализирует логгер параметрами.
    """
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    HTTPConnection.debuglevel = 1
    logging.basicConfig(
        level=logging.INFO,
        filename=f"{LOG_FOLDER}/{LOG_FILE_NAME}",
        encoding=LOG_ENCODING,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.INFO)
    requests_log.propagate = True


def get_logger():
    """
    Возвращает логгер для записи.
    """
    _init_logger()
    return logging.getLogger(__name__)
