"""
Обновление записи в таблицее User.
"""

from db.super_prize.sql import SuperPrizeTemplate


def get_update_count_template():
    template = SuperPrizeTemplate.update_count

    return template.render()
