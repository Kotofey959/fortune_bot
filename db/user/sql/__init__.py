"""
Сырые шаблоны таблицы.
"""

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("db/user/sql"))


class UserTemplate:
    """
    Шаблоны таблицы User.
    """

    select = env.get_template("select.sql")
    insert = env.get_template("insert.sql")
    update_spin_available = env.get_template("update_spin_available.sql")
    update_spin_usage = env.get_template("update_spin_usage.sql")
