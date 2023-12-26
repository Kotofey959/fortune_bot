"""
Обновление записи в таблицее User.
"""

from db.super_prize.sql import SuperPrizeTemplate


def get_select_count_template():

    template = SuperPrizeTemplate.select_count

    return template.render()
