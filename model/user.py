"""
Модель пользователя

"""
from aiogram import Bot
from environs import Env

from db.main import database
from db.user.insert import get_insert_template
from db.user.select import get_select_template
from db.user.update import get_update_spin_available_template, get_update_spin_usage_template
from helper.list import get_first_elem
from helper.referal import split_ref_link, build_ref_link

env = Env()
env.read_env()


class UserModel:
    """
    Модель пользователя.
    """

    def __init__(self, pk_id=None, ref_link=None) -> None:
        self.pk_id = pk_id
        self._ref_link = ref_link

        self._record: dict = None

    @property
    def record(self) -> dict:
        """
        Возвращает информацию по модели.
        """
        if self._record is None:
            self._record = self._get_record()

        return self._record

    def _get_record(self) -> dict:
        """
        Инфа по пользователю.
        """
        template = get_select_template({"telegram_id": self.pk_id} if not self._ref_link
                                       else {"ref_link": self._ref_link})
        sql_res = database.select_as_dict(template)
        return get_first_elem(sql_res)

    async def create(self, bot: Bot) -> None:
        """
        Создает пользователя по его идентификатору.
        """
        ref_link = await bot.create_chat_invite_link(chat_id=env("CHAT_ID"))
        template = get_insert_template(self.pk_id, ref_link=split_ref_link(ref_link.invite_link))
        database.execute(template)
        self._record = self._get_record()

    @property
    def available_spins(self):
        """
        Вовзращает количество доступных прокрутов пользователя

        :return:
        """
        spin_available = self.record.get("spin_available")
        return spin_available or 0

    @property
    def usage_spins(self):
        """
        Возвращает количество прокрутов пользователя

        :return:
        """
        spin_usage = self.record.get("spin_usage")
        return spin_usage or 0

    def change_spin_count(self, count_spin=1):
        """
        Изменяем количество доступных прокрутов

        :return:
        """
        template = get_update_spin_available_template(self.record.get("telegram_id"), count_spin)
        database.execute(template)
        self._record = self._get_record()

    def change_spin_usage_count(self, count_spin=1):
        """
        Изменяем количество использованных прокрутов пользователя

        :param count_spin:
        :return:
        """
        template = get_update_spin_usage_template(self.record.get("telegram_id"), count_spin)
        database.execute(template)
        self._record = self._get_record()

    @property
    def ref_link(self):
        """
        Получение реферальной ссылки пользователя

        :return:
        """
        if not self._ref_link:
            self._ref_link = self.record.get("ref_link")
        return build_ref_link(self._ref_link)
