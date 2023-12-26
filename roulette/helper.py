"""
Вспомогательные методы рулетки

"""
from db.main import database
from db.super_prize.select_count import get_select_count_template
from db.super_prize.update_count import get_update_count_template
from roulette.prizes import PRIZE_LIST


def get_prize_list():
    template = get_select_count_template()
    super_prize_count = database.fetchone(template)
    if super_prize_count < 5:
        return PRIZE_LIST
    else:
        return PRIZE_LIST[1:]


def update_super_prize_count():
    template = get_update_count_template()
    database.execute(template)