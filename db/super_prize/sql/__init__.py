"""
Сырые шаблоны таблицы.
"""

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("db/super_prize/sql"))


class SuperPrizeTemplate:
    """
    Шаблоны таблицы super_prize.
    """

    select_count = env.get_template("select_count.sql")
    update_count = env.get_template("update_count.sql")