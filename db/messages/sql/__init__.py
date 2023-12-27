"""
Сырые шаблоны таблицы.
"""

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("db/messages/sql"))


class MessagesTemplate:
    """
    Шаблоны таблицы User.
    """

    select = env.get_template("select.sql")
    insert = env.get_template("insert.sql")
