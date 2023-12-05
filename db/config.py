"""
Данные для входа в бд

"""
from environs import Env

env = Env()
env.read_env()


class DatabaseConfiguration:
    """
    Класс конфигурации базы данных.
    """

    HOST = env("DB_HOST")
    PORT = env("DB_PORT")
    USERNAME = env("DB_USER")
    PASSWORD = env("DB_PASSWORD")
    NAME = env("DB_NAME")
