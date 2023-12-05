"""
Подключение к базе данных

"""
import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor

from db.config import DatabaseConfiguration
from helper.list import get_first_elem
from helper.string import remove_spaces
from logger import get_logger

LOGGER = get_logger()


class DatabaseConnector:
    """
    Класс выполнения запросов к базе данных.
    """

    def __init__(self):
        self.host = DatabaseConfiguration.HOST
        self.username = DatabaseConfiguration.USERNAME
        self.password = DatabaseConfiguration.PASSWORD
        self.port = DatabaseConfiguration.PORT
        self.dbname = DatabaseConfiguration.NAME

        self._conn = None

    @property
    def connection(self) -> psycopg2.extensions.connection:
        """
        Возвращает подключение к БД.
        """
        if self._conn is None:
            self.__set_connection()
        return self._conn

    def __set_connection(self) -> None:
        """
        Открывает подключение к БД.
        """
        try:
            self._conn = psycopg2.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                port=self.port,
                dbname=self.dbname,
            )
        except psycopg2.DatabaseError as e:
            LOGGER.critical("Ошибка подключения к БД", exc_info=True)
            raise e
        finally:
            LOGGER.info(f"Подключение к БД {self.host}:{self.port}.")

    def select(self, query):
        """
        Выполняет запрос SELECT.
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    cursor.execute(query)
                    record_set = list(cursor.fetchall())
                    return record_set
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

    def select_as_dict(self, query) -> list[dict]:
        """
        Выполняет запрос SELECT и возвращает результат в виде списока словарей.
        """
        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                try:
                    LOGGER.info(remove_spaces(query))
                    cursor.execute(query)
                    record_set = cursor.fetchall()
                    LOGGER.info(f"RESULT (select_as_dict): {record_set}")
                    return record_set
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

    def execute(self, query):
        """
        Выполняет запрос без возврата значения.
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    cursor.execute(query)
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

    def fetchone(self, query):
        """
        Выполняет запрос возвращает единственное значение
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    cursor.execute(query)
                    record_set = cursor.fetchone()
                    elem = get_first_elem(record_set)
                    LOGGER.info(f"RESULT fetchone: {elem}")
                    return elem
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex


database = DatabaseConnector()
